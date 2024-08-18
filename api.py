from flask import *
from settings import *
from model import *
from lib import *
app = Blueprint(APP_NAME + "-api","api",url_prefix="/api")
@app.route("/add",methods=["POST"])
@app.route("/add/",methods=["POST"])
def add():
    dbname = request.args.get("db","goods")
    print(request.form,request.args)
    if dbname == "goods":
        if lin(["name","tag_id","company","count"],request.form):
            good = Goods()
            good.name = request.form["name"]
            good.tag_id = int(request.form["tag_id"])
            good.company = request.form["company"]
            good.count = int(request.form["count"])
            db.session.add(good)
        else:
            return jsonify({"status":"BadRequest"}),400
    elif dbname == "tag":
        if lin(["name"],request.form):
            tag = Tag()
            tag.name = request.form["name"]
            db.session.add(tag)
        else:
            return jsonify({"status":"BadRequest"}),400
    elif dbname == "log":
        if lin(["type","good_id","count"],request.form):
            log = Log()
            log.type = int(request.form["type"])
            log.good_id = int(request.form["good_id"])
            log.count = int(request.form["count"])
            db.session.add(log)
        else:
            return jsonify({"status":"BadRequest"}),400
    elif dbname == "messageq":
        if lin(["message","category"],request.form):
            message = MessageQ()
            message.message = request.form["message"]
            message.category = request.form["category"]
            db.session.add(message)
        else:
            return jsonify({"status":"BadRequest"}),400
    db.session.commit()
    return jsonify({"status":"OK"})
@app.route("/query",methods=["GET"])
@app.route("/query/",methods=["GET"])
def query():
    dbname = request.args.get("db","goods")
    if dbname == "goods":
        q = Goods.query
        if "id" in request.args:
            q = q.filter(Goods.id == int(request.args["id"]))
        if "name" in request.args:
            q = q.filter(Goods.name == request.args["name"])
        if "tag_id" in request.args:
            q = q.filter(Goods.tag_id == int(request.args["tag_id"]))
        if "company" in request.args:
            q = q.filter(Goods.company == request.args["company"])
        if "count" in request.args:
            q = q.filter(Goods.count == int(request.args["count"]))
    elif dbname == "tag":
        q = Tag.query
        if "id" in request.args:
            q = q.filter(Tag.id == int(request.args["id"]))
        if "name" in request.args:
            q = q.filter(Tag.name == request.args["name"])
    elif dbname == "log":
        q = Log.query.order_by(Log.id.desc())
        if "id" in request.args:
            q = q.filter(Log.id == int(request.args["id"]))
        if "type" in request.args:
            q = q.filter(Log.type == int(request.args["type"]))
        if "good_id" in request.args:
            q = q.filter(Log.good_id == int(request.args["good_id"]))
        if "date" in request.args:
            q = q.filter(Log.date.between(datetime.strptime(request.args["date"] + " 00:00:00","%Y/%m/%d %H:%M:%S"),datetime.strptime(request.args["date"] + " 23:59:59","%Y/%m/%d %H:%M:%S")))
        if "count" in request.args:
            q = q.filter(Log.count == int(request.args["count"]))
    elif dbname == "messageq":
        q = MessageQ.query.order_by(MessageQ.id.desc())
        if "id" in request.args:
            q = q.filter(MessageQ.id == int(request.args["id"]))
        if "message" in request.args:
            q = q.filter(MessageQ.message.like(f"%{request.args['message']}%"))
        if "category" in request.args:
            q = q.filter(MessageQ.category == int(request.args["category"]))
    elif dbname == "limit":
        q = Limit.query
    if q.count() > 0:
        return jsonify({"status":"OK","data":str(q.limit(1000).all()),"count":q.count()})
    else:
        return jsonify({"status":"NotFound","data":"[]","count":0}),404
@app.route("/delete",methods=["GET"])
@app.route("/delete/",methods=["GET"])
def delete():
    dbname = request.args.get("db","goods")
    id = request.args.get("id",None)
    if not id:
        return jsonify({"status":"BadRequest"}),400
    else:
        id = int(id)
    if dbname == "goods":
        obj = Goods.query.get(id)
        if obj:
            db.session.delete(obj)
    elif dbname == "tag":
        obj = Tag.query.get(id)
        if obj:
            db.session.delete(obj)
    elif dbname == "log":
        obj = Log.query.get(id)
        if obj:
            db.session.delete(obj)
    elif dbname == "messageq":
        obj = MessageQ.query.get(id)
        if obj:
            db.session.delete(obj)
    if obj:
        db.session.commit()
        return jsonify({"status":"OK"})
    else:
        return jsonify({"status":"NotFound"}),404
@app.route("/modify",methods=["POST"])
@app.route("/modify/",methods=["POST"])
def modify():
    dbname = request.args.get("db","goods")
    id = request.form.get("id",None)
    if not id:
        return jsonify({"status":"BadRequest"}),400
    if dbname == "goods":
        obj = Goods.query.get(id)
        if obj:
            if "name" in request.form:
                obj.name = request.form["name"]
            if "tag_id" in request.form:
                obj.tag_id = int(request.form["tag_id"])
            if "company" in request.form:
                obj.company = request.form["company"]
            if "count" in request.form:
                obj.count = int(request.form["count"])
                limit = Limit.query.get(obj.id)
                if limit:
                    if obj.count > limit.rlimit and limit.olimitstat != 2:
                        limit.olimitstat = 2
                        mq = MessageQ()
                        mq.message = f"货物{obj.name}已经超出上限，请尽快处理。"
                        mq.category = 2
                        db.session.add(mq)
                    elif obj.count < limit.llimit and limit.olimitstat != 1:
                        limit.olimitstat = 1
                        mq = MessageQ()
                        mq.message = f"货物{obj.name}已经低于下限，请尽快处理。"
                        mq.category = 2
                        db.session.add(mq)
                    elif obj.count > limit.llimit and obj.count < limit.rlimit and limit.olimitstat != 0:
                        limit.olimitstat = 0
                        mq = MessageQ()
                        mq.message = f"货物{obj.name}数量已经回复正常。"
                        mq.category = 1
                        db.session.add(mq)
    elif dbname == "tag":
        obj = Tag.query.get(id)
        if obj:
            if "name" in request.form:
                obj.name = request.form["name"]
    elif dbname == "log":
        obj = Log.query.get(id)
        if obj:
            if "type" in request.form:
                obj.type = request.form["type"]
            if "good_id" in request.form:
                obj.good_id = int(request.form["good_id"])
            # if "date" in request.form:
            #     obj.date = datetime.now()
            if "count" in request.form:
                obj.count = int(request.form["count"])
    elif dbname == "messageq":
        obj = MessageQ.query.get(id)
        if obj:
            if "message" in request.form:
                obj.message = request.form["message"]
            if "category" in request.form:
                obj.category = int(request.form["category"])
    if obj:
        db.session.commit()
        return jsonify({"status":"OK"})
    else:
        return jsonify({"status":"NotFound"}),404
@app.route("/setlimit",methods=["POST"])
@app.route("/setlimit/",methods=["POST"])
def set_limit():
    id = request.form.get("id",None)
    if not id:
        return jsonify({"status":"BadRequest"}),400
    id = int(id)
    good = Goods.query.get(id)
    if not good:
        return jsonify({"status":"NotFound"}),404
    addstat = False
    lim = Limit.query.get(id)
    if not lim:
        lim = Limit()
        lim.id = id
        lim.rlimit = 2147483647
        lim.llimit = -1
        addstat = True
    if "llimit" in request.form:
        lim.llimit = int(request.form["llimit"])
    if "rlimit" in request.form:
        lim.rlimit = int(request.form["rlimit"])
    if addstat:
        db.session.add(lim)
    db.session.commit()
    return {"status":"OK"}