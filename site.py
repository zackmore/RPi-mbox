#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import json

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

from tornado.options import options, define
define('port', default=8000, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/list/(\d+)', ListHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = scoped_session(sessionmaker(bind=engine))


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class MainHandler(BaseHandler):
    def get(self):
        return self.render('index.html')


class ListHandler(BaseHandler):
    def get(self, lid):
        q = self.db.query(Songs).filter(Songs.lid==lid).order_by(Songs.order)
        songs = []
        for song in q:
            songs.append(song.toDict())
        songs = json.dumps(songs)
        self.write(songs)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
