#!/usr/bin/env python
import os
import simplejson as json
import feedparser
import urllib2
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
        entries = mc.get('rss')
        
        if not entries:
            entries = feedparser.parse(blog_rss).entries
            mc.set('rss', entries, 3600)

        return entries
              
    except Exception, e:
        raise e


def getTwitterNbFollowers(username):
    """Retrieve the number of followers, then put it in the damn cache bitch"""
    try:
        nb_followers = mc.get('twitter')
        
        if not nb_followers:
            url = ''.join(['https://api.twitter.com/1/users/show.json?screen_name=', username])
            result = json.loads(urllib2.urlopen(url).read())
            nb_followers = result['followers_count']
            # 10min cache
            mc.set('twitter', nb_followers, 600)

        return nb_followers
    except Exception, e:
        raise e
        

def getDribbbleShots(username, count=3):
    """Retrieve last Dribbble shots, then again memcache its ass off"""
    try:
        dribbble_shots = mc.get('dribbble')
        
        if not dribbble_shots:
            url = ''.join(['http://api.dribbble.com/players/', username, '/shots'])
            result = json.loads(urllib2.urlopen(url).read())
            dribbble_shots = result['shots'][:count]
            # 1 hour cache
            mc.set('dribbble', dribbble_shots, 3600)
            
        return dribbble_shots
    except Exception, e:
        raise e