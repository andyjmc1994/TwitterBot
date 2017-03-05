#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
import json
import logging
import warnings
from pprint import pprint
 
warnings.filterwarnings("ignore")
 
ACCESS_KEY = '742723184869449732-XR1728Hy0o8narA9enMDMIO6KCMStRf'
ACCESS_SECRET = 'H46IGs5yCX23QL7lfdorXCe1atjiCnSRRDhiFaFyNTFYX'
CONSUMER_KEY = '6A785fwmkEbTbNN72WIvrEuQC'
CONSUMER_SECRET = 'ospKQiKqITsEdG3mQfcR6132xoRia23pzD1b5ZtaSigaLLXFmJ'
 
auth_handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth_handler.set_access_token(ACCESS_KEY , ACCESS_SECRET)
 
twitter_client = API(auth_handler)
 
logging.getLogger("main").setLevel(logging.INFO)
 
AVOID = ["monty", "leather", "skin", "bag", "blood", "bite"]
 
 
class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = True
            for word in AVOID:
                if word in tweet['text'].lower():
                    logging.info("SKIPPED FOR {}".format(word))
                    publish = False
 
            if tweet.get('lang') and tweet.get('lang') != 'en':
                publish = False
 
            if publish:
                twitter_client.retweet(tweet['id'])
                logging.debug("RT: {}".format(tweet['text']))
 
        except Exception as ex:
            logging.error(ex)
 
        return True
 
    def on_error(self, status):
        print status
 
 
if __name__ == '__main__':
    listener = PyStreamListener()
    stream = Stream(auth_handler, listener)
    stream.filter(track=['retweet to win tickets', 'retweet to win euro','RT to win euro','win euro 2016','win euro2016','win england tickets', 'euro 2016 tickets'])
 
