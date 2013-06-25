#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import options, define
define('port', default=8000, help='run on the given port', type=int)
define('mp3files', default=os.path.join(os.path.dirname(__file__), 'mp3'), help='mp3 files path')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render('index.html')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
