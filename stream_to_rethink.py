#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from oauth2client.client import SignedJwtAssertionCredentials
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import rethinkdb as r
from  rethinkdb import ReqlRuntimeError

# Twitter
token = ""
token_key = ""
con_secret = ""
con_secret_key = ""
# RethinkDB
r.connect('localhost', 28015).repl()
try:
    r.db_create('twitter').run()
    r.db('twitter').table_create('tweet').run()
except ReqlRuntimeError:
    pass

class MyStreamListener(StreamListener):
    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        if 'text' in json_data:
            print(json.dumps(json_data))
            tweet_id = json_data["id"]
            r.db('twitter').table('tweet').insert(json_data).run()
            return True
        return False

    def on_error(self, status_code):
        print(status_code)


auth = OAuthHandler(con_secret, con_secret_key)
auth.set_access_token(token, token_key)

twitterStream = Stream(auth, MyStreamListener())
twitterStream.filter(locations=[139.60, 35.60, 139.90, 35.80])
