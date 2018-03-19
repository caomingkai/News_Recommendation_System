# -*- coding: utf-8 -*-

import os
import sys
from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..',  'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://tfeocjao:0PdOdeoktaClt0RkaZu599GQFy3h3PmX@otter.rmq.cloudamqp.com/tfeocjao"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://panlrosv:6t9QmCluxc1VJotrrpkD7yz2Wj63k7OB@otter.rmq.cloudamqp.com/panlrosv"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return
    task = msg
    text = None

    '''
    # We shift to 'article' below, since XPath can only support CNN
    if task['source'] == 'cnn':
        print 'Scraping CNN news'
        text = cnn_news_scraper.extract_news(task['url'])
    else:
        print 'News source [%s] is not supported .' % task['source']
    '''
    article = Article(task['url'])
    article.download()
    article.parse()

    print article.text

    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)

while True:
    # fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                print '------------------- < Fetcher Begin > is fetching msg--------------------------'
                handle_message(msg)
                print '------------------- < Fetcher End > has done with fetching msg-----------------'
            except Exception as e:
                print '## Fetcher Exception: %s' % e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
