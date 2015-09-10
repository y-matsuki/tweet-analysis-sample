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
