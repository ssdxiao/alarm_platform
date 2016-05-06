
import tornado.web

class StaticHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("../static/luyin.html") 

