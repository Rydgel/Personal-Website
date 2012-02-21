#!/usr/bin/env python
import os
import feedparser
import pylibmc

mc = pylibmc.Client(
    servers=[os.environ.get('MEMCACHE_SERVERS', '127.0.0.1')],
    username=os.environ.get('MEMCACHE_USERNAME', None),
    password=os.environ.get('MEMCACHE_PASSWORD', None),
    binary=True
)

def getRSS(blog_rss):
    """We take all the RSS entries and we put them in memcache for 1 hour"""
    try:
        if mc.get("rss"):
            entries = mc.get("rss")
        else:
            entries = feedparser.parse(blog_rss).entries
            mc.set("rss", entries, 3600)

        return entries
              
    except Exception, e:
        raise e
    