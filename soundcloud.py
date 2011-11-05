from optparse import OptionParser
import mechanize
import re

def open_page(url):
    return mechanize.urlopen(url)

def get_stream_token_uid(page):
    """ returns stream token and uid as tuple """
    match = re.search('"uid":"([\w\d]+?)".*?stream_token=([\w\d]+)', page)
    if match:                               
        uid = match.group(1)
        stream_token = match.group(2)
        return (uid, stream_token)

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-u", "--url")
    (options, args) = parser.parse_args()

    cj = mechanize.LWPCookieJar()
    opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
    mechanize.install_opener(opener)

    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    browser.open(options.url)
    html = browser.response().get_data()

    # HOW GET COOKIE?

    #page = open_page(options.url).read()
    #(uid, stream_token) = get_stream_token_uid(page)

    #url = "http://media.soundcloud.com/stream/%s?stream_token=%s" % (uid, stream_token)




