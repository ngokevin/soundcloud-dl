from optparse import OptionParser
import re
from browser_clone import url_open

def get_stream_url(page):
    """ returns stream token and uid as tuple """
    match = re.search('http://media.soundcloud.com/stream/.*?(?=\")', page)
    if match:
        return match.group(0)

def get_song_title(page):
    match = re.search('(?<=\"title\":\").*?(?=\")', page)
    if match:
        return match.group(0)

def download(stream_url, song_title):
    """ given url with token and uid, download file to mp3 """
    response = url_open(stream_url)
    song_file = song_title + '.mp3'

    f = open(song_file, 'w')
    f.write(response.read())

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-u", "--url")
    (options, args) = parser.parse_args()
    if not options.url:
        print "Need to give a URL silly"
    else:
        # open up initial page (argument) to get stream token and uid
        response = url_open(options.url)
        html = response.read()
        stream_url = get_stream_url(html)
        song_title = get_song_title(html)
        print song_title

        # the browser does this...so we will too
        #response = url_open('http://media.soundcloud.com/crossdomain.xml')

        # compose a url with uid and token and request the mpeg
        #download(stream_url)
