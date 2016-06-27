#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
import tornado.web
from base import BASEDIR
from utils.log import log
import os
from database import db
from utils.mysqlpasswd import mysql_password
import uuid
import json
from utils.record import save_record

from base import authenticated_self

class UploadHandler(BaseHandler):


    def get(self):
        log.debug("UploadHandler get in")



    def post(self):
        log.debug("UploadHandler post in")
        if self.request.files == {}:
            result = {}
            result["error"] = "null file upload"
            self.send_data(result)
            return
        file_metas = self.request.files['file']# 提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filename = meta['filename']
            upload_path = "./static/audio"
            filepath = os.path.join(upload_path, filename)
            log.debug("write %s"%filepath)
            with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
        result = {}
        result["result"] = "ok"
        self.send_data(result)





