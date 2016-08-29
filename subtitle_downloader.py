#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name      : subtitle downloader
# Authors   : Maroof Ahmad
#-------------------------------------------------------------------------------
import os
import sys
import hashlib
import urllib2
import requests,time,re,zipfile
from bs4 import BeautifulSoup

#this hash function receives the name of the file and returns the hash code
def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def try_opensubtitles(file_path):
    try:
        root,ext = os.path.splitext(file_path)
        if ext not in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",".3g2"]:
            return

        if not os.path.exists(root + ".srt"):
            # root2 = root
            # root2 = root2.split("\\")[-1]
            j=-1
            root2=root
            for i in range(0,len(root)):
                if(root[i]=="\\"):
                    j=i
            root=root2[j+1:]
            root2=root2[:j+1]
            res = requests.get("http://www.opensubtitles.org/en/search2/sublanguageid-eng/moviename-"+root)
            soup = BeautifulSoup(res.content,"lxml")

            link=soup.find_all('a',attrs={'class':'bnone'})[0].get("href")
            res = requests.get("http://www.opensubtitles.org"+link)
            soup = BeautifulSoup(res.content,"lxml")
            link=soup.find_all('a',attrs={'class':'bnone'})[0].get("href")
            res = requests.get("http://www.opensubtitles.org"+link)
            soup = BeautifulSoup(res.content,"lxml")
            final_link=soup.find_all('a',attrs={'id':'bt-dwl-bt'})[0].get("href")
            res = requests.get("http://www.opensubtitles.org"+final_link)
            soup = BeautifulSoup(res.content,"lxml")
            print res.content
            subfile=open(root2+".zip", 'wb')
            for chunk in res.iter_content(100000):
                subfile.write(chunk)
                subfile.close()
                time.sleep(1)
                zip=zipfile.ZipFile(root2+".zip")
                zip.extractall(root2)
                zip.close()
                os.unlink(root2+".zip")
                os.rename(root2+zip.namelist()[0], os.path.join(root2, root + ".srt"))

    except:
        print("Error in fetching subtitle for " + file_path)
        print("Error", sys.exc_info())

def download(file_path):
    #download subtitle using subdb api
    try:
        root,ext = os.path.splitext(file_path)
        if ext not in [".avi", ".mp4", ".mkv", ".mpg", ".mpeg", ".mov", ".rm", ".vob", ".wmv", ".flv", ".3gp",".3g2"]:
            return

        if not os.path.exists(root + ".srt"):
            headers = {'User-Agent':'SubDB/1.0 (subtitle-downloader/1.0; https://github.com/maroof-ahmad/subtitle_downloader)'}
            url = 'http://api.thesubdb.com/?action=download&hash='+get_hash(file_path)+'&language=en'
            req = urllib2.Request(url, '', headers)
            response = urllib2.urlopen(req).read()
            with open(root + ".srt", "wb") as subtitle:
                subtitle.write(response)
    except:
        try_opensubtitles(file_path)


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
