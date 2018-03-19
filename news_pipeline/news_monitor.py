# -*- coding: utf-8 -*-

import datetime
import hashlib
import os
import redis
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..',  'common'))
import news_api_client
from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 24 * 3600
# There is rate limit: 1000 for 24 hours
# Sleep cloudAMQP every 5 min to defer the NewsAPI call
# Totally 11 sources => 11 API calls a time
# 1000 / 11 = 90 times
# Means: no matter what the sleep time is, we should limit frequency the following block executes to 90 times a day

SLEEP_TIME_IN_SECONDS = 5 * 60

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://panlrosv:6t9QmCluxc1VJotrrpkD7yz2Wj63k7OB@otter.rmq.cloudamqp.com/panlrosv'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'tap-news-scrape-news-task-queue'

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

redis_client = redis.StrictRedis( REDIS_HOST, REDIS_PORT )
cloudAMQP_client = CloudAMQPClient( SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME )

newsapi_call_num = 0

while True:
    newsapi_call_num += 1
    print '------------------- < Monitor Begin > call New API : # %d -------------------------' % newsapi_call_num
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    print '------------------- < Monitor End > call New API : # %d ---------------------------' % newsapi_call_num

    num_of_new_news = 0

    for news in news_list:
        # convert article into Hash value by MD5, in order to make duplication check easier
        # encode() make special symbol compatible with our check system
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:  # in case this filed doesn't show up
                # "2018-03-16T19:13:35Z" YYYY-MM-DDTHH:MM:SS in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)
    print 'Fetched %d new news.' % num_of_new_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
