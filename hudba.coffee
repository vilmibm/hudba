# This program is distributed under the terms
# of the GNU General Public License
# Copyright 2010 Nathaniel Smith

sys = require('sys')
fs  = require('fs')

print = (string) -> sys.print string + "\n"

class Library
    constructor: (path) -> @path = path

    is_music_file : (path) ->
        return (err, stats) =>
            if stats.isDirectory()
                @scan(path)
            else
                print 'found file: ' + path
                # execve into tags2json.py
                # got tags?
                # mongo logic
                # push to client

    scan: (path) ->
        path ?= @path
        fs.readdir(path, (err, files) =>
            for filename in files
                abspath = path + '/' + filename
                fs.stat(abspath, @is_music_file(abspath))
        )

library = new Library('/home/nate/Music')

library.scan()
