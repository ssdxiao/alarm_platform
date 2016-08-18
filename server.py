#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
import time
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

try:
    import simplejson as json
except ImportError:
    import json


from app.login import LoginHandler
from app.login import LogoutHandler
from app.alarm import AlarmHandler
from app.alarm import AlarmAllHandler
from app.custumer import CustumerHandler
from app.custumer import CustumerAllHandler
from app.manage import ManageHandler
from app.manage import ManageAllHandler
from app.manage import ManageChangePasswordHandler
from app.record import RecordAllHandler
from app.audio import AudioHandler
from app.audio import AudioAllHandler
from app.upload import UploadHandler
from app.alarm import EventsHandler
from utils.log import log
from utils.config import SERVERPORT
from utils.config import MAIN_URL

from app.database import DB

from app.base import BaseHandler
from app.base import authenticated_self
from app.httpclient import HttpClient

LISTENERS = []
AUDIO_PATH = "/tmp/audio"



client = HttpClient(MAIN_URL)

def alarm_sync():
    db =DB()
    client.get_token()
    while True:
        try:
            time.sleep(10)
            lastid = db.get_sync_id()
            events = client.get_alarm(lastid)
            if events == None:
                client.get_token()
                continue
            else:
                if events == []:
                    #log.debug("not has any event")
                    continue
                for one in events:
                    print one
                    db.save_event(one["id"], one["type"],one["deviceid"],one["zwavedeviceid"],one["eventtime"],one["objparam"])
        except:
            import traceback
            traceback.print_exc()
            continue


class RedirectHandler(tornado.web.RequestHandler):
    def get(self):
        log.debug("RedirectHandler")
        self.redirect("/static/index.html")
        pass

db =DB()
class ReleaseAlarmHandler(BaseHandler):
    @authenticated_self
    def post(self):
        log.debug("ReleaseAlarmHandler post in")
        data = self.get_data()
        if data:
            log.debug(data)
            if data.has_key("alarmId"):
                zwaveid = db.get_zwaveid_from_alarm(data["alarmId"])
                result = {}
                result["result"] = "ok"
                self.send_data(result)

                client.releasealarm(zwaveid, self.login_user)
                return
            else:
                result = {}
                result["result"] = "error"
                result["message"] = "data is error"
                self.send_data(result)



settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    'auto_reload': True,
    "cookie_secret": "61oETzKXQAGaYdkL5g3mGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/static/error.html",
    'debug': True,
}

application = tornado.web.Application([
    ('/app/login', LoginHandler),
    ('/app/logout', LogoutHandler),
    ('/app/alarm', AlarmHandler),
    ('/app/alarmlist', AlarmAllHandler),
    ('/app/custumer', CustumerHandler),
    ('/app/custumerlist', CustumerAllHandler),
    ('/app/manage', ManageHandler),
    ('/app/managelist', ManageAllHandler),
    ('/app/manage/changepasswd', ManageChangePasswordHandler),
    ('/app/recordlist', RecordAllHandler),
    ('/app/audio', AudioHandler),
    ('/app/audiolist', AudioAllHandler),
    ('/app/upload', UploadHandler),
    ('/app/events', EventsHandler),
    ('/server/releasealarm', ReleaseAlarmHandler),
    #('/static/(.*)', StaticHandler),
    ('/.*', RedirectHandler),
], **settings)

#chrome --allow-running-insecure-content
# usage from http://stackoverflow.com/questions/8045698/https-python-client
# openssl genrsa -out privatekey.pem 2048
# openssl req -new -key privatekey.pem -out certrequest.csr
# openssl x509 -req -in certrequest.csr -signkey privatekey.pem -out certificate.pem
if __name__ == "__main__":
    threading.Thread(target=alarm_sync).start()
    http_server = tornado.httpserver.HTTPServer(
        application,
        #ssl_options={
        #    "certfile": os.path.join("./", "certificate.pem"),
        #    "keyfile": os.path.join("./", "privatekey.pem"),
        #}
    )

    http_server.listen(SERVERPORT)
    log.info("server start")
    tornado.ioloop.IOLoop.instance().start()
