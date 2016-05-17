
import tornado.web
from base import BaseHandler
from base import BASEDIR
class StaticHandler(BaseHandler):
    def get(self, html):
        url = "%s/%s"%(BASEDIR,html)
        try :
            self.render(url)
        except:
            self.redirect("/static/index.html")


