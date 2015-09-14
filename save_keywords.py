#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import rethinkdb as r

r.connect('localhost', 28015).repl()
dic_csv = open('data/my_dict.csv', 'w')

if __name__ == '__main__':
    from_time = int(time.mktime((datetime.today() - timedelta(days=1)).timetuple()) * 1000)
    to_time = int(time.mktime(datetime.today().timetuple()) * 1000)
    cursor = r.db('mecab').table('dict').between(
        from_time, to_time, index='time').order_by(
        index=r.desc('time')).limit(10).run()
    for item in cursor:
        dic_csv.write(''.join([item['word'], u",,,,名詞,一般,*,*,*,*,", item['word'], ',,\n']).encode('utf-8'))
