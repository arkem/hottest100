"""
TODO:
- interface with mayer via named pipe 
- implement limit
- pagination of results
- randomisation of tracks
- looping in interactive mode
"""

import urllib
import urllib2
import re
import htmllib
import os
import sys

search_page     = 'http://www.youtube.com/results?search_query='
search_phrase   = ""
limit           = 40
home_dir        = "~/"
prog_dir        = ".mytube"
playlist        = []
delim           = "/^^||^^/"
video_output    = ""

def strip_tags(value):
    "Return the given HTML with all tags stripped."
    return re.sub(r'<[^>]*?>', '', value) 

def fetch(url):
    r = urllib2.Request(url)
    response = urllib2.urlopen(r)
    html = response.read()
    return html

def unescape(s):
    try:
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(s)
        return p.save_end()
    except Exception, e:
        print "Error in unescape(): %s" % e
        return ""

def search(search_phrase,limit):
    global playlist
    global delim

    search_phrase = re.sub(" ","+",search_phrase)
    search_url    = search_page + search_phrase
    print search_url
    r             = fetch(search_url)
    video_link    = re.compile("""
                    .*href="/watch.v=
                    ([^"]*)"              #video id
                    \s*rel="nofollow">
                    <img\s*title="
                    ([^"]*)               #title
                    """,re.VERBOSE|re.I)

    count = 1
    for line in r.split('\n'):
        m = re.match(video_link, line)
        if m:
            video_id = m.group(1)
            title = m.group(2)
            #print "%s\t%s" % (count, title)
            playlist.append("%s%s%s" % (video_id, delim, title))
            count += 1
    playlist_select(playlist)


def play_song(video_id,title):
    global video_output

    t_value = re.compile(""".*swfArgs.*
                            "t":\s*
                            "([^"]*)"
                         """,re.VERBOSE|re.I)

    url = "http://youtube.com/watch?v=%s" % (video_id)
    print url
    result = fetch(url)
    for line in result.split('\n'):
        m = re.match(t_value, line)
        if m:
            url = "%s/get_video.php?l=165&video_id=%s&t=%s" \
                  % ("http://youtube.com", video_id, m.group(1))
            print url

    os.system("mplayer %s \"%s\"" % (video_output, url))
    #urllib.urlretrieve(url, dl_dir + "/" + torrent_num + ".torrent")

def playlist_select(playlist):
    global delim

    for i in range(1, len(playlist)):
        print "%s:\t%s" % (i, playlist[i].split(delim)[1])
    response = input("Enter number to play: ")
    (video_id,title) = playlist[int(response)].split(delim)
    play_song(video_id, title)

for i in range(1,len(sys.argv)):
    if sys.argv[i].startswith("-l"):
        limit = int(sys.argv[i].lstrip("-l"))
        continue
    elif sys.argv[i].startswith("-n"):
        video_output = "-vo null"
        continue
    search_phrase += sys.argv[i] + " "

search_phrase = search_phrase.rstrip(" ")
search(search_phrase,limit)
