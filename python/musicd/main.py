import tornado.httpserver
import tornado.ioloop
import tornado.web
import pymongo
import fnmatch
import thread
import time
import json
import re
import os

from mutagen.oggvorbis import OggVorbis
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

import Config

connection = pymongo.Connection()
db         = connection.musicd
tracks     = db.musicd

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """
            This is the no update version of musicd, so we read the FS once at
            load to sync the DB and then load the tracks into a template.

            A page refresh is necessary to reflect changes in the track listing.
        """
        library_path = os.path.normpath(Config.absolute_library)

        for root, dirs, files in os.walk(library_path):
            for filename in fnmatch.filter(files, "*.ogg") + fnmatch.filter(files, "*.mp3"):
                path = os.path.join(root, filename)
                track = {}
                try:
                    if re.search(".ogg", filename):
                        audio = OggVorbis(path)
                        track['length'] = audio.info.length
                    elif re.search(".mp3", filename):
                        audio = EasyID3(path)
                        track['length'] = MP3(path).info.length
                except:
                    print "Failed to read tags: %s" % path
                    continue

                for key in audio.keys():
                    if key in Config.tags:
                        track[key] = audio[key].pop()

                track['path'] = re.sub(library_path+'/', '', path)

                spec = {}
                for tag in ['artist','album','title']:
                    if tag in track:
                        spec[tag] = track[tag]

                if not tracks.find_one(spec):
                    print "found %s" % track['path']
                    tracks.save(track)

        # look for deleted files
        for track in tracks.find():
            path = os.path.join(library_path, track['path'])
            if not os.path.exists(path):
                print "deleting from db: %s" % path
                tracks.remove(track)

        self.render("main.html", tracks=tracks.find(
            fields = Config.tags,
            sort   = [
                ("artist", pymongo.ASCENDING),
                ("album", pymongo.ASCENDING)
            ]
        ))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/static/(.*)",
        tornado.web.StaticFileHandler, 
        {"path":os.path.join(os.path.dirname(__file__), "static")}),
    (r"/(.*)",
        tornado.web.StaticFileHandler, {"path":Config.absolute_library}),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
