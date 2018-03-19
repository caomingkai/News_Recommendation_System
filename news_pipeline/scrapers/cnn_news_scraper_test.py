
import cnn_news_scraper as scraper

EXPECTED_STRING = "The storms were expected to move into Alabama Sunday evening and continue along a path extending to Michigan."
CNN_NEWS_URL = "http://www.cnn.com/2017/04/30/us/severe-weather-tornadoes-flooding/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)
    print news
    assert EXPECTED_STRING in news
    print 'test_basic passed!'

if __name__ ==  "__main__":
    test_basic()
