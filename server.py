#!/usr/bin/python
# -*- coding: utf-8 -*-

import web


urls = ( '/', 'index' ) 
class index: 
    def GET(self): 
        return "Hello, world!" 




application = web.application(urls, globals()).wsgifunc()
if __name__ == "__main__":
    pass

