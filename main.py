from flask import *
from model import *
from lib import *
from settings import *
from flask_migrate import Migrate
import api
app = Flask(APP_NAME)
for conf in CONFIGS:
    app.config[conf] = CONFIGS[conf]
db.init_app(app)
migrate = Migrate(app,db)
app.register_blueprint(api.app)
@app.after_request
def requestprocess(res):
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Headers"] = "*"
    return res
if __name__ == "__main__":
    app.run(HOST,PORT)