#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
import threading
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
import sys
import time
import random
from datetime import datetime


try:
    import simplejson as json
except ImportError:
    import json
import shutil
import urllib2
import urllib

from app.static import StaticHandler
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

from app.database import db

LISTENERS = []
AUDIO_PATH = "/tmp/audio"

URL="https://test.isurpass.com.cn/iremote"
user="thirdparter_tecus"
password="2c9c8047fbef41b3b496b8553eb1e1fa897314"

class HttpClient:
    def __init__(self, url, timeout=10):
        self.url = URL

    def post(self, url, values):

        try:
            url = self.url + url
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            data= response.read()
            log.debug(data)
            data = json.loads(data)
            return data
        except:
            print "post request error"
            return None


    def get_token(self):
        values = {'code': user, 'password': password}
        data = self.post("/thirdpart/login", values)
        if data :
            if data["resultCode"] == 0:
                return data["token"]
            else:
                print "get token error"

        return None

    def get_alarm(self,id, token):
        values = {'lastid': id, 'token': token}
        data = self.post("/thirdpart/event/queryevent", values)
        if data:
            if data["resultCode"] == 0:
                if data.has_key("events"):
                    return data["events"]
                else:
                    return []
            else:
                print "get token error"

        return None


client = HttpClient(URL)

def alarm_sync():
    token = client.get_token()
    while True:
        time.sleep(1)
        lastid = db.get_sync_id()
        print"*"*20
        events = client.get_alarm(lastid,token)
        if events == None:
            token = client.get_token()
            continue
        else:
            if events == []:
                log.debug("not has any event")
                continue
            for one in events:
                try:
                    print one
                    if one["objparam"] == {}:
                        print "#"*20
                        content=""
                    else:
                        content = one["objparam"]["content"]
                    print content
                    db.save_event(one["id"], one["type"],one["deviceid"],one["zwavedeviceid"],one["eventtime"],content)
                except:
                    break

                if lastid < one["id"]:
                        lastid = one["id"]

            db.save_sync_id(lastid)


class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        LISTENERS.append(self)
        self.user_id = 0

    def send_data(self, data):
        log.debug( "send data")
        #try:
        data = json.dumps(data)

        self.write_message(data)
        return "ok"
        #except:
         #   log.error("send not json (%s)" % data)

    def send_alarm(self, one):
        data = {"type": "alarm",
                "id": one[0]
                }
        self.send_data(data)

    def on_message(self, message):
        log.debug(message)
        try:
            data = json.loads(message)
        except:
            log.error("ws recv not json")

        if data.has_key("id"):
            log.debug("websocket user %s has login"%data["id"])
            self.user_id = data["id"]

    def on_close(self):
        LISTENERS.remove(self)
        print "close"


class RedirectHandler(tornado.web.RequestHandler):
    def get(self):
        log.debug("RedirectHandler")
        self.redirect("/static/index.html")
        pass


class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        log.debug("PageNotFoundHandler")
        self.redirect("/static/index.html")

tornado.web.ErrorHandler = PageNotFoundHandler


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
    ('/server/realtime', RealtimeHandler),
    ('/app/upload', UploadHandler),
    ('/app/events', EventsHandler),
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

    http_server.listen(80)
    log.info("server start")
    tornado.ioloop.IOLoop.instance().start()
