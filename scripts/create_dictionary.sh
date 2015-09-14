#!/bin/sh
python save_keywords.py
/usr/local/libexec/mecab/mecab-dict-index -m ../mecab/mecab-ipadic-2.7.0-20070801.model -d ../mecab-ipadic-2.7.0-20070801 -u data/my_dict_with_cost.csv -f utf-8 -t utf-8 -a data/my_dict.csv
/usr/local/libexec/mecab/mecab-dict-index -m ../mecab/mecab-ipadic-2.7.0-20070801.model -d ../mecab-ipadic-2.7.0-20070801 -u data/my_dict.dic -f utf-8 -t utf-8 data/my_dict_with_cost.csv
