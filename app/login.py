from base import BaseHandler
from base import BASEDIR
from utils.log import log
from base import authenticated_self
from database import DB
from utils.mysqlpasswd import mysql_password
import uuid

db = DB()
class LoginHandler(BaseHandler):

    def post(self):
        log.debug("login come")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("user") and data.has_key("passwd"):
                passwd = db.get_user_by_passwd(data["user"]);
                log.debug(" mysql passwd %s  passwd %s"%(mysql_password(data["passwd"]),passwd))
                if mysql_password(data["passwd"]) == passwd:
                    token = uuid.uuid1()
                    db.set_token(data["user"], token)
                    result ={}
                    result["result"] = "ok"
                    result["user"] = data["user"]
                    result["token"] = str(token)
                    self.send_data(result)
                    return
                else:
                    log.error("password  %s is not correct"%data["passwd"])
            else:
                log.error("not has user or passwd ")
        else:
            log.error("data is none")

        result = {}
        result["result"] = "error"
        result["message"] = "user or passwd is not correct"
        self.send_data(result)

class LogoutHandler(BaseHandler):
    @authenticated_self
    def post(self):
        log.debug("logout come")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("user") and data.has_key("token"):
                token = db.get_token(data["user"]);
                log.debug(" mysql  token %s  token %s"%(token,data["token"]))
                if token == data["token"]:
                    db.del_token(data["user"])
                    result ={}
                    result["result"] = "ok"
                    result["user"] = data["user"]
                    self.send_data(result)
                    return
                else:
                    log.error("logout  token %s is not correct"%data["token"])
            else:
                log.error("logout not has user or token ")
        else:
            log.error("data is none")

        result = {}
        result["result"] = "error"
        result["message"] = "user or token is not correct"
        self.send_data(result)