from main import *
with app.app_context():
    db.drop_all()
    db.create_all()
    good = Goods()
    good.company = "演示厂商"
    good.tag_id = 1
    good.name = "演示货品"
    good.count = 100
    tag = Tag()
    tag.name = "演示标签"
    db.session.add(good)
    db.session.add(tag)
    db.session.commit()