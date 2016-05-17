import tornado.web
from utils.log import log
BASEDIR = "../static"
import json

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #log.debug("has coming %s"% self.get_secure_cookie("user"))
        self.get_secure_cookie("user") == "test"
        return False

    def get(self):
        self.redirect("/static/index.html")
        pass

    def get_data(self):
        try:
            data = json.loads(self.request.body)
            return data
        except:
            log.error("get not json (%s) "%self.request.body )
            return None

    def send_data(self, data):
        try:
            data = json.dumps(data)
            self.write(data)
            return "ok"
        except:
            log.error("send not json (%s)"% data)