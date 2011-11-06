#!/usr/bin/env/ python

from optparse import OptionParser
import cookielib
import urllib2
import sys
import re

# set up header values and openers
header_values =  {'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16', 'Accept' : 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding' : 'gzip,deflate,sdch', 'Accept-Language' : 'en-US,en;q=0.8', 'Cache-Control' : 'max-age=0', 'Connection' : 'keep-alive'}
cj = cookielib.MozillaCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
urllib2.install_opener(opener)

def open_url(url):
    retry = 0;
    while retry < 3:
        request = urllib2.Request(options.url, headers=header_values)
        response = opener.open(request)
        html = response.read()
        if not html:
            retry += 1
            continue
        break
    return html

def get_stream_token_uid(page):
    """ returns stream token and uid as tuple """
    match = re.search('"uid":"([\w\d]+?)".*?stream_token=([\w\d]+)', page)
    if match:                               
        uid = match.group(1)
        stream_token = match.group(2)
        return (uid, stream_token)

def get_song_title(page):
    match = re.search('(?<=\"title\":\").*?(?=\")', page)
    if match:
        return match.group(0)

def download(uid, token, song_title='soundcloud_dl.mp3'):
    """ given url with token and uid, download file to mp3 """

    url = "http://media.soundcloud.com/stream/%s?stream_token=%s" % (uid, token)
    request = urllib2.Request(url, headers=header_values)
    response = opener.open(request)

    f = open(song_title, 'w')
    f.write(response.read())

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-u", "--url", help="soundcloud url to download", dest="url")
    (options, args) = parser.parse_args()
    if not options.url:
        parser.error("--url option requires an argument")
    
    # open up initial page to get stream token, uid, song title
    html = open_url(options.url)
    if not html:
        print "could not fetch html"
        sys.exit()
    uid, token = get_stream_token_uid(html)
    song_title = get_song_title(html) + '.mp3' 

    # the browser does this...so we will too
    open_url('http://media.soundcloud.com/crossdomain.xml')

    # compose a url with uid and token and request the mpeg 
    download(uid, token, song_title)




