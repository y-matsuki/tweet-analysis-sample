#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, math

import rethinkdb as r
from  rethinkdb import ReqlRuntimeError
import MeCab

r.connect('localhost', 28015).repl()
try:
    r.db_create('mecab').run()
    r.db('mecab').table_create('dict').run()
except ReqlRuntimeError:
    pass


def extract_keyword(text):
    tagger = MeCab.Tagger()
    keywords = []
    if text.startswith("I'm at "):
        return []
    splited_text = text.split():
    splited_text = [ v for v in splited_text if not v.startswith('@') ]
    splited_text = [ v for v in splited_text if not v.startswith('#') ]
    splited_text = [ v for v in splited_text if not v.startswith('http') ]
    text = ' '.join(splited_text)
    encoded_text = text.encode('utf-8')
    node = tagger.parseToNode(encoded_text).next
    tmp = []
    while node:
        if node.feature.split(',')[0] == "名詞":
            tmp.append(node.surface)
        if node.feature.split(',')[0] != "名詞":
            if len(tmp) > 1:
                keywords.append("".join(tmp))
            del tmp[:]
        node = node.next
    if len(tmp) > 1:
        keywords.append("".join(tmp))
    keywords = [ v for v in keywords if not v == '' ]
    keywords = [ v for v in keywords if not v.startswith('http') ]
    return keywords

def handle_stream():
    cursor = r.db('twitter').table('tweet').filter(
            {'lang': 'ja'}).pluck('text').changes().run()
    for document in cursor:
        text = document['new_val']['text']
        keywords = extract_keyword(text)
        print(text)
        print(", ".join(keywords))
        for keyword in keywords:
            json_data = {
                'word': unicode(keyword, ('utf-8')),
                'text': text,
                'time': math.floor(time.time() * 1000)
            }
            r.db('mecab').table('dict').insert(json_data).run()
        print('----')


if __name__ == '__main__':
    handle_stream()
