#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from decorators import cached
import simplejson as json
import feedparser
import urllib2


@cached(3600, 'rss')
def getRSS(blog_rss):
    """We take all the RSS entries and we put them in memcache for 1 hour"""
    try:
        return feedparser.parse(blog_rss).entries
                   
    except Exception, e:
        print "RSS Exception"
        return None


@cached(600, 'twitter')
def getTwitterNbFollowers(username):
    """Retrieve the number of followers, then put it in the damn cache bitch"""
    try:
        url = 'https://api.twitter.com/1/users/show.json?screen_name=' + username
        result = json.loads(urllib2.urlopen(url).read())
        return result['followers_count']

    except Exception, e:
        print "Twitter Exception"
        return 0
        

@cached(3600, 'dribbble')
def getDribbbleShots(username, count=3):
    """Retrieve last Dribbble shots, then again memcache its ass off"""
    try:
        url = 'http://api.dribbble.com/players/' + username + '/shots'
        result = json.loads(urllib2.urlopen(url).read())
        return result['shots'][:count]
        
    except Exception, e:
        print "Dribbble Exception"
        return None