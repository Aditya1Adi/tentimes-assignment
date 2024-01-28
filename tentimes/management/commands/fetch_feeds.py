from django.core.management.base import BaseCommand
import feedparser
from textblob import TextBlob
from tentimes.models import NewsArticle
from datetime import datetime
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def parse_rss_date(date_str):
    try:
        pub_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
    except ValueError:
        try:
            pub_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
        except ValueError:
            logger.warning(f"Failed to parse date string: {date_str}")
            pub_date = datetime.now()
    return pub_date

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

class Command(BaseCommand):
    help = 'Fetch and parse news feeds'

    def handle(self, *args, **options):
        feeds = [
            "http://rss.cnn.com/rss/cnn_topstories.rss",
            "http://qz.com/feed",
            "http://feeds.foxnews.com/foxnews/politics",
            "http://feeds.reuters.com/reuters/businessNews",
            "http://feeds.feedburner.com/NewshourWorld",
            "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
        ]

        for feed_url in feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                try:
                    title = entry.title

                    # Extract content using BeautifulSoup to remove HTML tags
                    soup = BeautifulSoup(entry.summary, 'html.parser')
                    content = soup.get_text()

                    pub_date_str = entry.get('published') or entry.get('pubDate') or ''
                    pub_date = parse_rss_date(pub_date_str)
                    source_url = entry.link

                    # Analyze sentiment
                    sentiment_score = analyze_sentiment(title + " " + content)

                    # Check for duplicate articles
                    if not NewsArticle.objects.filter(title=title, pub_date=pub_date).exists():
                        NewsArticle.objects.create(
                            title=title,
                            content=content,
                            pub_date=pub_date,
                            source_url=source_url,
                            sentiment_score=sentiment_score
                        )
                except Exception as e:
                    logger.error(f"Error processing entry: {e}")
                    continue
