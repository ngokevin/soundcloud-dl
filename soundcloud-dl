#!/usr/bin/python
from optparse import OptionParser
import cookielib
import urllib2
import random
import time
import sys
import re

# max number of download attempts
max_retry = 3

# set up header values and openers
header_values =  {'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16', 'Accept' : 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding' : 'gzip,deflate,sdch', 'Accept-Language' : 'en-US,en;q=0.8', 'Cache-Control' : 'max-age=0', 'Connection' : 'keep-alive'}
cj = cookielib.MozillaCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
urllib2.install_opener(opener)

def open_url(url):
    """ fetches html from given url """
    print "fetching html..."
    try:
        request = urllib2.Request(url, headers=header_values)
        response = opener.open(request)
    except urllib2.HTTPError, e:
        time.sleep(1)
    except ValueError, e:
        print str(e)
        return None
    html = response.read()
    return html

def get_stream_token_uid(page):
    """ returns stream token and uid as tuple """
    match = re.search('"uid":"([\w\d]+?)".*?stream_token=([\w\d]+)', page)
    if match:
        uid = match.group(1)
        stream_token = match.group(2)
        return (uid, stream_token)

def get_song_title(page):
    """ scrapes song title from soundcloud link """
    match = re.search('(?<=\"title\":\").*?(?=\")', page)
    if match:
        return match.group(0).replace(' ','_')
    else:
        alpha = "abcdefghijklmnopqrstuvwxyz"
        random_length = 5
        return ''.join(random.choice(alpha) for i in xrange(random_length))

def get_soundcloud_links(url):
    """ given an url , scrape and return list of soundcloud links """
    retry = 0
    while True:
        if retry == max_retry:
            return None

        html = open_url(url)
        if not html:
            retry += 1
            print "could not fetch html. (%s) " % (retry)
            continue
        break
    return ['http://soundcloud.com' + url for url in re.findall('<h3><a href="(/.*?)">.*?</a></h3>', html)]

def download(uid, token, song_title):
    """ given url with token and uid, download file to mp3 """

    # compose a url with uid and token and request the mpeg
    url = "http://media.soundcloud.com/stream/%s?stream_token=%s" % (uid, token)
    request = urllib2.Request(url, headers=header_values)
    response = opener.open(request)

    f = open(song_title + '.mp3', 'w')
    f.write(response.read())

def main(**kwargs):
    """ takes in an url or url to page to scrape soundcloud links """
    
    url = kwargs['url']

    retry = 0
    while True:

        if retry == max_retry:
            print "failed to download song"
            sys.exit(1)

        # open up initial page to get stream token, uid, song title
        html = open_url(url)
        if not html:
            retry += 1
            print "Could not retrieve initial html. (%s) " % (retry)
            continue 
        
        # get stream token returns none if html is random binary 
        info = get_stream_token_uid(html)
        if not info:
            retry += 1
            print "Could not get stream token. (%s)" % (retry)
            continue 

        (uid, token) = info
        song_title = get_song_title(html)
        break 

    # the browser does this...so we will too
    open_url('http://media.soundcloud.com/crossdomain.xml')

    download(uid, token, song_title)
    print song_title + " successfully downloaded."

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-u", "--url", help="soundcloud url to download", dest="url")
    parser.add_option("-p", "--page", help="downloads all soundcloud urls found in given page", dest="page_url")
    (options, args) = parser.parse_args()

    urls = []
    if options.page_url:
        urls = get_soundcloud_links(options.page_url)
    if options.url:
        urls.append(options.url) 
    if not options.url and options.page_url:
        print "USAGE: soundcloud.py [-u URL] [-p PAGE WITH URLS]"

    print "downloading: " + str(urls)
    for url in urls:
        main(**{'url':url})


