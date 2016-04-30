#!/usr/bin/python
# -*- coding: utf-8 -*-

import web


urls = ( '/', 'index',
         '/login', 'login',
 ) 
class index: 
    def GET(self): 
        raise web.seeother('/static/login.html') 




application = web.application(urls, globals()).wsgifunc()
if __name__ == "__main__":
    pass

