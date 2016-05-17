from base import BaseHandler
from base import BASEDIR
from utils.log import log

from database import DB
from utils.mysqlpasswd import mysql_password
import uuid

db = DB()
class CustumerHandler(BaseHandler):

    def post(self):
        log.debug("CustumerHandler post in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("CustumerTelephone") and data.has_key("CustumerEmail") \
                    and data.has_key("CustumerName") and data.has_key("CustumerRemark"):
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


