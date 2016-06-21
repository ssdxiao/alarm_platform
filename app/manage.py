from base import BaseHandler
from base import BASEDIR
from utils.log import log

from database import DB
from utils.mysqlpasswd import mysql_password
import uuid
import json

from base import authenticated_self
db = DB()
class ManageHandler(BaseHandler):

    @authenticated_self
    def get(self):
        log.debug("ManageHandler get in")
        try:
            id = int(self.get_argument("id"))
        except:
            log.debug("param id is not int")
            return
        data = db.get_manage(id)
        result = {}
        if data:

            result["result"] = "ok"
            result["data"] = {"manageid" : data[0],
                                        "managename" : data[1],
                                        "managetelephone" : data[2]
                                       }

        else:
            result["result"] = "error"
            result["message"] = "can not find this user"

        self.send_data(result)

    @authenticated_self
    def post(self):
        log.debug("ManageHandler post in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("ManageTelephone") and data.has_key("ManagePassword") \
                    and data.has_key("ManageName") :

                if data["ManageName"] == "":
                    log.error("ManageName is NULL")
                else:
                    db.insert_manage(data["ManageName"], data["ManageTelephone"],
                                   data["ManagePassword"])


                    result ={}
                    result["result"] = "ok"
                    self.send_data(result)
                    return

            else:
                log.error("Manaage data key is not right")
        else:
            log.error("data is none")

        result = {}
        result["result"] = "error"
        result["message"] = "Manaage info is error"
        self.send_data(result)

    @authenticated_self
    def put(self):
        log.debug("ManageHandler put in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("ManageTelephone") and data.has_key("ManageId") \
                    and data.has_key("ManageName"):
                db.update_manage(data["ManageId"],data["ManageName"], data["ManageTelephone"])
                result = {}
                result["result"] = "ok"
                self.send_data(result)
                return
            else:
                result = {}
                result["result"] = "error"
                result["message"] = "data is error"
                self.send_data(result)





class ManageAllHandler(BaseHandler):
    @authenticated_self
    def get(self):
        log.debug("ManaageAllHandler get in")
        try:
            index = int(self.get_argument("index"))
        except:
            index = 1
        if index > 0:
            pass
        else:
            index = 1

        data = db.get_manage_list(index)
        result = {}
        if data:
            result["result"] = "ok"
            result["maxindex"] = data["maxindex"]
            result["curruntindex"] = data["curruntindex"]
            result["data"] =[]
            for one in data["data"]:
                result["data"].append({"manageid" : one[0],
                                        "managename" : one[1],
                                        "managetelephone" : one[2],
                                        "managelogintime": one[5],
                                       "managelogouttime": one[6]
                                       })

            self.send_data(result)

        else:

            result["result"] = "error"
            result["message"] = "get Manage list failed"
            self.send_data(result)

class ManageChangePasswordHandler(BaseHandler):

    @authenticated_self
    def put(self):
        log.debug("ManageChangePasswordHandler put in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("ManagePassword") and data.has_key("ManageId"):
                db.update_manage_passwd(data["ManageId"],data["ManagePassword"])
                result = {}
                result["result"] = "ok"
                self.send_data(result)
                return
            else:
                result = {}
                result["result"] = "error"
                result["message"] = "data is error"
                self.send_data(result)

