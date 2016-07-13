#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

import tornado.web
import os

import time
import random
import tornado.websocket
import tornado.httpserver

try:
    import simplejson as json
except ImportError:
    import json

from utils.log import websocketlog as log

from app.database import db

LISTENERS = []
"""
该服务负责推送消息，并从数据库检查没有分配的告警进行分配，同时周期性将未处理的任务推送给前端
"""
def alarm_allocation():
    while True:
        time.sleep(10)
        data = db.get_alarm_unallocat()
        manage = db.get_online_manage()

        if manage:
            num = int(len(manage))
            if data and manage:
                for one in data:
                    db.allocat_alarm(one[0], manage[random.randint(0, num - 1)][0])

        data = db.get_alarm_unprogress()
        if data:
            for one in data:
                for person in LISTENERS:
                        if person.user_id == one[0]:
                            person.send_alarm(one)



class RealtimeHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        LISTENERS.append(self)
        log.debug("open")
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


settings = {
    'auto_reload': True,
    "cookie_secret": "61oETzKXQAGaYdkL5g3mGeJJFuYh7EQnp2XdTP1o/Vo=",
    'debug': True,
}

application = tornado.web.Application([
    ('/server/realtime', RealtimeHandler),
], **settings)

#chrome --allow-running-insecure-content
# usage from http://stackoverflow.com/questions/8045698/https-python-client
# openssl genrsa -out privatekey.pem 2048
# openssl req -new -key privatekey.pem -out certrequest.csr
# openssl x509 -req -in certrequest.csr -signkey privatekey.pem -out certificate.pem
if __name__ == "__main__":
    threading.Thread(target=alarm_allocation).start()
    http_server = tornado.httpserver.HTTPServer(
        application,
        ssl_options={
            "certfile": os.path.join("./", "certificate.pem"),
            "keyfile": os.path.join("./", "privatekey.pem"),
        }
    )

    http_server.listen(443)
    log.info("websocket server start")
    tornado.ioloop.IOLoop.instance().start()
