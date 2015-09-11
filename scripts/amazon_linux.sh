#!/bin/bash

# Install MeCab
sudo yum install -y gcc* make
wget https://mecab.googlecode.com/files/mecab-0.996.tar.gz
tar xzvf mecab-0.996.tar.gz
cd mecab-0.996
./configure --with-charset=utf-8
make
sudo make install
sudo bash -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/usr-local.conf'
## cleanup
cd ..
rm mecab-0.996.tar.gz

# Install MeCab IPA dictionary
wget https://mecab.googlecode.com/files/mecab-ipadic-2.7.0-20070801.tar.gz
tar zxvf mecab-ipadic-2.7.0-20070801.tar.gz
cd mecab-ipadic-2.7.0-20070801
./configure --with-charset=utf-8
make
sudo make install
## cleanup
cd ..
rm mecab-ipadic-2.7.0-20070801.tar.gz

# Install mecab-python
wget https://mecab.googlecode.com/files/mecab-python-0.996.tar.gz
tar xavf mecab-python-0.996.tar.gz
cd mecab-python-0.996
sed -i "s/mecab-config/\/usr\/local\/bin\/mecab-config/g" setup.py
sudo python setup.py build
sudo python setup.py install
sudo sh -c 'echo /usr/local/lib >> /etc/ld.so.conf'
sudo ldconfig
## test
python test.py
## cleanup
cd ..
rm mecab-python-0.996.tar.gz

# Install User Dictionary
sudo wget http://mirror.centos.org/centos/6/os/x86_64/Packages/nkf-2.0.8b-6.2.el6.x86_64.rpm
sudo rpm -ivh nkf-2.0.8b-6.2.el6.x86_64.rpm
sudo rm nkf-2.0.8b-6.2.el6.x86_64.rpm
wget https://mecab.googlecode.com/files/mecab-ipadic-2.7.0-20070801.model.bz2
bzip2 -d mecab-ipadic-2.7.0-20070801.model.bz2
sed -i "s/charset: euc-jp/charset: utf-8/g" mecab-ipadic-2.7.0-20070801.model
nkf -w --overwrite mecab-ipadic-2.7.0-20070801.model
nkf -w --overwrite mecab-ipadic-2.7.0-20070801/*.def

# Create User Dictionary
echo '東京特許許可局,,,,名詞,一般,*,*,*,*,とうきょうとっきょきょかきょく,トウキョウトッキョキョカキョク,トウキョウトッキョキョカキョク' >> my_dic.csv
# コストの計算
/usr/local/libexec/mecab/mecab-dict-index\
 -m ../mecab-ipadic-2.7.0-20070801.model\
 -d ../mecab-ipadic-2.7.0-20070801\
 -u my_dic_with_cost.csv\
 -f utf-8\
 -t utf-8\
 -a my_dic.csv
# 辞書の作成
/usr/local/libexec/mecab/mecab-dict-index\
 -m ../mecab-ipadic-2.7.0-20070801.model\
 -d ../mecab-ipadic-2.7.0-20070801\
 -u my_dic.dic\
 -f utf-8\
 -t utf-8\
 -a my_dic_with_cost.csv
cp /usr/local/etc/mecabrc ~/.mecabrc
echo "userdic = $(pwd)/my_dic.dic" >> ~/.mecabrc
