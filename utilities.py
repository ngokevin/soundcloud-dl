#!/usr/bin/env python

from browser_clone import url_open
import re

def get_stream_url(page):
    """ returns stream token and uid as tuple """
    match = re.search('http://media.soundcloud.com/stream/.*?(?=\")', page)
    if match:
        return match.group(0)

def get_song_title(page):
    match = re.search('(?<=\"title\":\").*?(?=\")', page)
    if match:
        return match.group(0)

def download(song_url):
    """ given url with token and uid, download file to mp3 """

    # open up initial page (argument) to get stream token and uid
    response = url_open(song_url)
    html = response.read()
    stream_url = get_stream_url(html)
    song_title = get_song_title(html)

    # the browser does this...so we will too
    response = url_open('http://media.soundcloud.com/crossdomain.xml')

    response = url_open(stream_url)
    song_file = song_title + '.mp3'

    f = open(song_file, 'w')
    f.write(response.read())
