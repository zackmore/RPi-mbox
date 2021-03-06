#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import json
import subprocess
import time

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

from tornado.options import options, define
define('port', default=8000, help='run on the given port', type=int)
define('mp3path', default=os.path.join(os.path.dirname(__file__), 'static/mp3/'))
define('mpSocket', type=object)


###
### Functional Class
###
class MPlayer:
    '''
    A simple mplayer class to interactive mplayer
    command requires: pause, stop, loadfile and so on.
    '''
    def __init__(self):
        self._mplayer = subprocess.Popen(
                            ['mplayer', '-slave', '-quiet', '-idle'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE
                        )
        self._pid = self._mplayer.pid

    def command(self, name, *args):
        cmd = '%s%s%s\n'%(name,
                    ' ' if args else '',
                    ' '.join(repr(a) for a in args)
                )
        self._mplayer.stdin.write(cmd)
        if name == 'quit':
            return


###
### App Base
###
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/list/(\d+)', ListHandler),
            (r'/playnew', PlayNewHandler),
            (r'/playnew/control', ControlHandler),
            (r'/kill', KillHandler),
            (r'/addnewsong', AddNewSongHandler),
            (r'/test', TestHandler),
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


class MPlayerHandler(BaseHandler):
    def createMPlayer(self):
        return MPlayer()


###
### App Handler
###
class MainHandler(BaseHandler):
    def get(self):
        self.render('index.html')


class ListHandler(BaseHandler):
    def get(self, lid):
        q = self.db.query(Songs).filter(Songs.lid==lid).order_by(Songs.order)
        songs = []
        for song in q:
            songs.append(song.toDict())
        songs = json.dumps(songs)
        self.write(songs)


class PlayNewHandler(MPlayerHandler):
    def post(self):
        sid = self.get_argument('sid')
        pid = self.get_argument('pid')

        song = self.db.query(Songs).filter(Songs.sid==sid).one()
        mp3url = options.mp3path + song.mp3url
        if not options.mpSocket:
            options.mpSocket = self.createMPlayer()
            #self.write(str(options.mpSocket._mplayer.pid))
        options.mpSocket.command('loadfile '+mp3url)


class ControlHandler(BaseHandler):
    def post(self):
        options.mpSocket.command('pause')


class KillHandler(BaseHandler):
    def post(self):
        options.mpSocket.command('stop')
        options.mpSocket.command('exit')
        options.mpSocket._mplayer.terminate()


class AddNewSongHandler(BaseHandler):
    def post(self):
        song = dict(zip(['name', 'mp3url', 'imageurl', 'lid'],
                    [self.get_argument('name'), self.get_argument('url'),
                    self.get_argument('image'), self.get_argument('list')
                    ]))
        #song = Songs(**song)
        #self.db.add(song)
        #self.db.flush()
        self.write(json.dumps(song))


class TestHandler(BaseHandler):
    def get(self):
        pass


###
### run
###
if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
