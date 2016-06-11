from base import BaseHandler
from base import BASEDIR
from utils.log import log

from database import DB
from utils.mysqlpasswd import mysql_password
import uuid
import json

db = DB()
class CustumerHandler(BaseHandler):

    def get(self):
        log.debug("CustumerHandler get in")
        try:
            id = int(self.get_argument("id"))
        except:
            log.debug("param id is not int")
            return
        data = db.get_custumer(id)
        result = {}
        if data:

            result["result"] = "ok"
            result["data"] = {"custumerid" : data[0],
                                        "custumername" : data[1],
                                        "custumertelephone" : data[2],
                                        "custumeremail" : data[3],
                                        "custumerremark": data[4],
                                        "other":json.loads(data[5])
                                       }

        else:
            result["result"] = "error"
            result["message"] = "can not find this user"

        self.send_data(result)



    def post(self):
        log.debug("CustumerHandler post in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("CustumerTelephone") and data.has_key("CustumerEmail") \
                    and data.has_key("CustumerName") and data.has_key("CustumerRemark"):

                if data["CustumerName"] == "":
                    log.error("CustumerName is NULL")
                else:
                    db.insert_custumer(data["CustumerName"], data["CustumerTelephone"],
                                   data["CustumerEmail"],data["CustumerRemark"])


                    result ={}
                    result["result"] = "ok"
                    self.send_data(result)
                    return

            else:
                log.error("custumer data key is not right")
        else:
            log.error("data is none")

        result = {}
        result["result"] = "error"
        result["message"] = "custumer info is error"
        self.send_data(result)

    def put(self):
        log.debug("CustumerHandler put in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("CustumerTelephone") and data.has_key("CustumerEmail") \
                    and data.has_key("CustumerName") and data.has_key("CustumerRemark")\
                    and data.has_key("CustumerId")and data.has_key("other"):
                db.update_custumer(data["CustumerId"],data["CustumerName"], data["CustumerTelephone"],
                                   data["CustumerEmail"],data["CustumerRemark"],json.dumps(data["other"]))
                result = {}
                result["result"] = "ok"
                self.send_data(result)
                return
            else:
                result = {}
                result["result"] = "error"
                result["message"] = "data is error"
                self.send_data(result)





class CustumerAllHandler(BaseHandler):

    def get(self):
        log.debug("CustumerAllHandler get in")
        try:
            index = int(self.get_argument("index"))
        except:
            index = 1
        if index > 0:
            pass
        else:
            index = 1

        data = db.get_custumer_list(index)
        result = {}
        if data:
            result["result"] = "ok"
            result["maxindex"] = data["maxindex"]
            result["curruntindex"] = data["curruntindex"]
            result["data"] =[]
            for one in data["data"]:
                result["data"].append({"custumerid" : one[0],
                                        "custumername" : one[1],
                                        "custumertelephone" : one[2],
                                        "custumerremark": one[4]
                                       })

            self.send_data(result)

        else:

            result["result"] = "error"
            result["message"] = "get custumer list failed"
            self.send_data(result)


