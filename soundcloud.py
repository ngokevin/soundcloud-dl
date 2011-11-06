from optparse import OptionParser
from utilities import download

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-u", "--url")
    (options, args) = parser.parse_args()
    if not options:
        print "Need to give a URL silly"
    else:
        # compose a url with uid and token and request the mpeg
        if options.url:
            download(options.url)
