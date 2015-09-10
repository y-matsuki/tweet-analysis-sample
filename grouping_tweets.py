#!/usr/bin/python
# -*- coding: utf-8 -*-
from multiprocessing import Process

import rethinkdb as r

areas = [
    u"千代田区",u"中央区",u"港区",u"新宿区",u"文京区",
    u"台東区",u"墨田区",u"江東区",u"品川区",u"目黒区",
    u"太田区",u"世田谷区",u"渋谷区",u"中野区",u"杉並区",
    u"豊島区",u"北区",u"荒川区",u"板橋区",u"練馬区",
    u"足立区",u"葛飾区",u"江戸川区"
]


def handle_stream(place_name):
    r.connect('localhost', 28015).repl()
    cursor = r.db('twitter').table('tweet').filter(
            {'place':{'name': place_name}}
        ).pluck(
            'text',
            {'user':'screen_name'},
            {'place':'name'}
        ).changes().run()
    for document in cursor:
        print(document['new_val']['place']['name'])
        print(document['new_val']['text'])
        print('----')


if __name__ == '__main__':
    plist = []
    for area in areas:
        plist.append(Process(target=handle_stream, args=(area,)))
    for p in plist:
        p.start()
    for p in plist:
        p.join()
