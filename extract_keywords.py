#!/usr/bin/python
# -*- coding: utf-8 -*-
from multiprocessing import Process

import rethinkdb as r
from  rethinkdb import ReqlRuntimeError
import MeCab

r.connect('localhost', 28015).repl()
try:
    r.db_create('mecab').run()
    r.db('mecab').table_create('dict').run()
except ReqlRuntimeError:
    pass

def remove_blank(keywords):
    while True:
        try:
            keywords.remove("")
        except ValueError:
            break

def extract_keyword(raw_text):
    tagger = MeCab.Tagger()
    keywords = []
    for text in raw_text.split():
        if text.startswith('@') or text.startswith('#') or text.startswith('http'):
            continue;
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
        remove_blank(keywords)
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
                'text': text
            }
            r.db('mecab').table('dict').insert(json_data).run()
        print('----')


if __name__ == '__main__':
    handle_stream()
