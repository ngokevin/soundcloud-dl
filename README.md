## Soundcloud CLI tool
### Authors: ngokevin, uberj, thedjpetersen

edit: Soundcloud has been integrated into youtube-dl

A little command line tool for working with Soundcloud.

You can either pass in a direct URL to a Soundcloud song or you can pass in any
link that may possibly contain Soundcloud URLs and the script will scrape for 
the links and download them all at once. If you pass in both options, a page
and a URL, it would download the URL and any URLs found within the page.

USAGE: soundcloud.py -u [URL] -p [PAGE_WITH_URLs]

Also check out http://soundcloud-dl.com 
