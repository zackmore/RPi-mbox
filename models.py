#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship

from datetime import datetime
from time import time

Base = declarative_base()


class Songslist(Base):
    __tablename__ = 'songslist'

    lid = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


class Songs(Base):
    __tablename__ = 'songs'

    sid = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    mp3url = Column(String(100), nullable=False)
    imageurl = Column(String(100))
    order = Column(Integer, default=9999)
    lid = Column(None, ForeignKey('songslist.lid'))

    def __init__(self, sid=sid, name=name, mp3url=mp3url, imageurl=imageurl,
                order=order, lid=lid):
        self.sid = sid
        self.name = name
        self.mp3url = mp3url
        self.imageurl = imageurl
        self.order = order
        self.lid = lid

    def toDict(self):
        song = {
            'sid': self.sid,
            'name': self.name,
            'mp3url': self.mp3url,
            'imageurl': self.imageurl,
            'order': self.order,
            'lid': self.lid
        }
        return song


engine = create_engine('sqlite:///db/songs.sqlite3')

Base.metadata.create_all(engine)
