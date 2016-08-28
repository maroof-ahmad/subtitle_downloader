#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name      : subtitle downloader
# Authors   : Maroof Ahmad
#-------------------------------------------------------------------------------
import os
import sys
import hashlib
import urllib2

#this hash function receives the name of the file and returns the hash code
def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def download(file_path):
    #download subtitle using subdb api
    try:
        root,ext = os.path.splitext(file_path)
        if ext not in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",".3g2"]:
            return

        if not os.path.exists(root + ".srt"):
            headers = {'User-Agent':'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)'}
            url = 'http://api.thesubdb.com/?action=download&hash='+get_hash(file_path)+'&language=en'
            req = urllib2.Request(url, '', headers)
            response = urllib2.urlopen(req).read()
            with open(root + ".srt", "wb") as subtitle:
                subtitle.write(response)
    except:
        print "subtitle not found"


def readFileOrFolder():
    if(len(sys.argv) < 2):
        print "Please give the movie name file or folder"
        sys.exit(1)

    path,ext = os.path.splitext(sys.argv[1])
    if(ext is ''):
        #it is a folder
        if(os.path.isdir(path)):
            for dirname,subdirs,files in os.walk(path):
                for filename in files:
                    file_path = os.path.join(dirname,filename)
                    download(file_path)

        else:
            print "There is no directory with address ",path
    else:
        #it is a file
        download(path)


if __name__ == '__main__':
    readFileOrFolder()
