# tweet-analysis-sample

Twitter Streaming APIから取得したTweetをRethinkDBに蓄積して分析する

## Tweetの取得範囲

```javascript
// index.htmlの36,37行目の範囲を
new google.maps.LatLng(35.58, 139.60),
new google.maps.LatLng(35.80, 139.90))
// TweetStreamのフィルタに設定する
twitterStream.filter(locations=[139.60, 35.60, 139.90, 35.80])
```

## 実行手順

### 準備

```shell
pip install tweepy
pip install rethinkdb
git clone https://github.com/y-matsuki/tweet-analysis-sample.git
```

### RethinkDB起動

```shell
cd tweet-analysis-sample
mkdir -p data/rethink
rethinkdb --directory data/rethink
```

### Tweet収集起動

```shell
cd tweet-analysis-sample
python stream_to_rethink.py
```

### Tweet処理起動

```shell
cd tweet-analysis-sample
python grouping_tweets.py
```

### 確認(RethinkDB)

```javascript
// access to http://localhost:8080 and run.
r.db('twitter').table('tweet').getField('text').changes()
```
