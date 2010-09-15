sys = require('sys')
fs  = require('fs')

print = (string) -> sys.print string + "\n"

library = '/home/nate/bkp.Music'

scan = (library) ->
    fs.readdir(library, (err, files) ->
        for path in files
            fs.stat(library+'/'+path, is_music_file(library+'/'+path))
    )

is_music_file = (path) ->
    return (err, stats) ->
        if stats.isDirectory()
            scan(path)
        else
            print 'found file: ' + path
            # execve into tags2json.py
            # got tags?
            # mongo logic
            # push to client

scan(library)
