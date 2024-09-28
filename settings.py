APP_NAME = "Repository Management Server"
APP_VERSION = "1.0-240818-alpha"
CONFIGS = {
    "SQLALCHEMY_DATABASE_URI":"sqlite:///db.sqlite3",
    "SQLALCHEMY_TRACK_MODIFICATIONS":False
}
SECRETKEY = open("secret.key").read().strip("\n")
HOST = "0.0.0.0"
PORT = 35782