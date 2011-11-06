from optparse import OptionParser
import re
from browser_clone import url_open

def get_stream_token_uid(page):
    """ returns stream token and uid as tuple """
    match = re.search('"uid":"([\w\d]+?)".*?stream_token=([\w\d]+)', page)
    if match:
        uid = match.group(1)
        stream_token = match.group(2)
        return (uid, stream_token)

def download(uid, token):
    """ given url with token and uid, download file to mp3 """

    url = "http://media.soundcloud.com/stream/%s?stream_token=%s" % (uid, token)
    response = url_open(url)

    f = open('test.mp3', 'w')
    f.write(response.read())

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-u", "--url")
    (options, args) = parser.parse_args()

    # open up initial page (argument) to get stream token and uid
    response = url_open(options.url)
    html = response.read()
    (uid, token) = get_stream_token_uid(html)

    # the browser does this...so we will too
    response = url_open('http://media.soundcloud.com/crossdomain.xml')

    # compose a url with uid and token and request the mpeg
    download(uid, token)
