#!/usr/bin/env python
import urllib2
import re
import os
import sys

def strip_video(video_id):
    if video_id.find("youtube.com") != -1:
        url = video_id
        video_id = re.search("v=(\w*)", url).group(1) 
    else:
        url = "http://youtube.com/watch?v=%s" % (video_id)

    title = video_id

    t_value = re.compile(""".*swfArgs.*
                            "t":\s*
                            "([^"]*)"
                         """,re.VERBOSE|re.I)
    print url
    print video_id
    result = urllib2.urlopen(url).read()
    for line in result.split('\n'):
        m = re.match(t_value, line)
        if m:
            url = "%s/get_video.php?l=165&video_id=%s&t=%s&fmt=18" \
                  % ("http://youtube.com", video_id, m.group(1))
            print url
    try:        
        title = re.search("<title>(.*)</title>", result, re.M).group(1)
    except AttributeError:
        pass
    print 'Output: "%s.mp3"' % title

    os.system('mplayer -hardframedrop -vo null -cache 8096 -ao pcm:file="%s.pcm" "%s"' % (title, url))
    os.system('lame "%s.pcm" "%s.mp3"' % (title, title))
    os.system('rm "%s.pcm"' % title) # Dangerous

for s in sys.argv[1:]:
    strip_video(s)
