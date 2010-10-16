# This program is distributed under the terms
# of the GNU General Public License
# Copyright 2010 Nathaniel Smith

sys = require('sys')
fs  = require('fs')
exec = require('child_process').exec

tags2json = 'python ' + process.cwd() + '/../tags2json/tags2json.py'

print = (string) -> sys.print string + "\n"

class Library
    constructor: (path) -> @path = path

    process_file : (path) ->
        command = tags2json+' "'+path+'"'
        child = exec(command, (err, stdout, stderr) ->
            return unless stdout # no stdout means error or not music file
            eval "tags = " + stdout
            # mongo logic
            # push to client
        )

    _maybe_recur : (path) ->
        return (err, stats) =>
            if stats.isDirectory()
                @scan(path)
            else
                @process_file(path)

    scan: (path) ->
        path ?= @path
        fs.readdir(path, (err, files) =>
            files.forEach((filename) =>
                abspath = path + '/' + filename
                fs.stat(abspath, @_maybe_recur(abspath))
            )
        )

library = new Library('/home/nate/Music')

library.scan()
