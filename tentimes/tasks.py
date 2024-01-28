    # news/tasks.py

from celery import shared_task
from tentimes.models import NewsArticle
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

    # Download NLTK resource outside the task
nltk.download('vader_lexicon')

def classify_news_categories(combined_text, article_id):
        # Initialize SentimentIntensityAnalyzer
        sid = SentimentIntensityAnalyzer()

        # Perform sentiment analysis on the combined text
        sentiment_score = sid.polarity_scores(combined_text)

        # Assign category based on sentiment score
        if sentiment_score['compound'] >= 0.05:
            category = 'Positive/Uplifting'
        elif sentiment_score['compound'] <= -0.05:
            category = 'Terrorism/Protest/Political Unrest/Riot'
        else:
            category = 'Others'

        # Update the category in the database
        article = NewsArticle.objects.get(id=article_id)
        article.category = category
        article.save()