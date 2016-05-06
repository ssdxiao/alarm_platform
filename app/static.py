
import tornado.web

BASEDIR = "../static"
class StaticHandler(tornado.web.RequestHandler):
    def get(self, html):
        url = "%s/%s"%(BASEDIR,html)
        try :
            self.render(url)
        except:
            self.redirect("/static/index.html")


