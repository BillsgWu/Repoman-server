from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class Goods(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Unicode(64),unique=True,index=True)
    tag_id = db.Column(db.Integer)
    company = db.Column(db.Unicode(64))
    count = db.Column(db.Integer)
    def __repr__(self):
        return f'[{self.id},"{self.name}",{self.tag_id},"{self.company}",{self.count}]'
class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Unicode(64),unique=True,nullable=False)
    def __repr__(self):
        return f'[{self.id},"{self.name}"]'
class Log(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.Integer,nullable=False,default=0)
    # 0:进货
    # 1:出货
    good_id = db.Column(db.Integer,nullable=False)
    date = db.Column(db.DateTime,default=datetime.now)
    count = db.Column(db.Integer,default=1)
    def __repr__(self):
        return f'[{self.id},{self.type},{self.good_id},"{self.date.strftime("%Y/%m/%d %H:%M:%S")}",{self.count}]'
class MessageQ(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    message = db.Column(db.UnicodeText)
    category = db.Column(db.Integer)
    # 0:debug
    # 1:info
    # 2:warning
    # 3:error
    # 4:critical
    def __repr__(self):
        return f'[{self.id},"{self.message}",{self.category}]'
class Limit(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    llimit = db.Column(db.Integer)
    rlimit = db.Column(db.Integer)
    olimitstat = db.Column(db.Integer)
    # 0:normal
    # 1:llimit overcross
    # 2:rlimit overcross
    def __repr__(self):
        return f"[{self.id},{self.llimit},{self.rlimit}]"