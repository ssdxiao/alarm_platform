
import tornado.web
from base import BaseHandler
from base import BASEDIR
from utils.log import log
class StaticHandler(BaseHandler):
    def get(self, html):
        url = "%s/%s"%(BASEDIR,html)
        log.debug(url)
        #try :
        self.render(url)
        #except:
            #self.redirect("/static/index.html")


