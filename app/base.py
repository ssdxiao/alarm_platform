import tornado.web
from utils.log import log
BASEDIR = "../static"
import json
import functools
from database import DB
db=DB()

def authenticated_self(method):
    """Decorate methods with this to require that the user be logged in."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        cookie = self.request.headers.get('X-Auth')
        result = {}
        result["result"] = "error"
        result["message"] = "token error please login "

        if cookie:
            try:
                data = json.loads(cookie)
                print data
                if data.has_key("token"):
                    self.login_user = db.get_user_by_token(data["token"])
                    if self.login_user:
                        return method(self, *args, **kwargs)
            except:
                log.error("get error cookie %s",cookie)

        else:
            log.error("cookie is None")

        self.send_data(result)
        return

    return wrapper

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        #log.debug("has coming %s"% self.get_secure_cookie("user"))
        #log.debug("in this")

        #log.debug(type(self))
        result = {}
        result["result"] = "error"
        result["message"] = "token error please login "
        #self.send_data(result)
        return True

        #self.db.get_user_by_token()




    @staticmethod
    def get_login_user(func):
        def _deco(*args, **kwargs):
            print("before %s called." % func.__module__)

            ret = func(*args, **kwargs)
            print("  after %s called. result: %s" % (func.__name__, ret))
            return ret

        return _deco

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