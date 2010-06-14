import twitter
import urllib2
import re
import time
import subprocess
import sys

search_page     = 'http://www.youtube.com/results?search_query='
delim           = "/^^||^^/"

def fetch(url):
    r = urllib2.Request(url)
    response = urllib2.urlopen(r)
    html = response.read()
    return html

def search(search_phrase,limit):
    global delim
    search_phrase = re.sub(" ","+",search_phrase)
    search_url    = search_page + search_phrase
    print search_url
    r              = fetch(search_url)
    video_link     = re.compile('.*href="/watch.v=([^"]*)"', re.VERBOSE|re.I)
    for line in r.split('\n'):
        m = re.match(video_link, line)
        if m:
            video_id = m.group(1)
            return ("http://youtube.com/watch?v=%s" % video_id)

def getsong():
    twit = twitter.Twitter()
    r = twit.statuses.user_timeline(id="triplej")
    if len(r) > 1:
        for p in r:
            try:
                gr = re.match('#hottest100 no.(\d{0,3}) (.*) - (.*)',\
                              p["text"]).groups()
                if len(gr) == 3:
                    return (int(gr[0]), gr[1], gr[2])
            except:
                pass
    return (101, "", "")

def launch_browser(url):
    subprocess.Popen(["C:\\PATHTOCHROME\\chrome.exe", url])
    print url

current_number = 100
if len(sys.argv) > 1:
    current_number = int(sys.argv[1])

while(True):
    new_number, artist, title = getsong()
    print "%d %s %s" % (new_number, artist, title)
    if new_number < current_number:
	current_number = new_number
        url = search('"%s" "%s"' % (artist, title), 10)
        launch_browser(url)
    time.sleep(30)

