APP_NAME = "Repository Management Server"
APP_VERSION = "1.0-240818-alpha"
CONFIGS = {
    "SQLALCHEMY_DATABASE_URI":"mysql+pymysql://root:root@localhost/repoman",
    "SQLALCHEMY_TRACK_MODIFICATIONS":False
}
SECRETKEY = open("secret.key").read().strip("\n")
HOST = "0.0.0.0"
PORT = 35782
OUTSETTINGS = {}
# with open("outsettings",encoding="UTF-8") as file:
#     cont = file.read()
#     for line in cont.strip("\n").split("\n"):
#         OUTSETTINGS[line.split(":")[0]] = line.split(":")[1]