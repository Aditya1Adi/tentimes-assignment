

# News Article Classification System

## Overview
This project aims to build an application that collects news articles from various RSS feeds, stores them in a database, and categorizes them into predefined categories using natural language processing techniques. The application is developed in Python and utilizes several libraries and frameworks.

## Installation
1. Clone the repository:
   ```
   git clone <repository_url>
   ```

## Usage
1. **Feed Parser and Data Extraction:**
   - Run the script `fetch_feeds.py` to read the provided list of RSS feeds, parse each feed, and extract relevant information from each news article.
   ```
   python fetch_feeds.py
   ```
   - Ensures handling of duplicate articles from the same feed.

2. **Database Storage:**
   - Design a database schema to store the extracted news article data.
   - Implement logic to store new articles in the database without duplicates.

3. **Task Queue and News Processing:**
   - Set up Celery to manage asynchronous processing of new articles.
   - Configure the parser script to send extracted articles to the queue upon arrival.
   - Create a Celery worker that consumes articles from the queue and performs further processing:
     - Category classification using NLTK or spaCy.
     - Update the database with the assigned category for each article.

4. **Logging and Error Handling:**
   - Properly implement logging throughout the application to track events and potential errors.
   - Handle parsing errors and network connectivity issues gracefully.

## Database Schema
Your `NewsArticle` model provides a solid foundation for storing news article data. Here's a brief explanation of each field in the model:

1. **Title**: This field stores the title of the news article. It's a `CharField` with a maximum length of 255 characters, which should be sufficient to accommodate most titles.

2. **Content**: This field stores the main content of the news article. It's a `TextField`, allowing for longer text passages to be stored.

3. **pub_date**: This field stores the publication date and time of the news article. It's a `DateTimeField`, which accurately captures both the date and time.

4. **source_url**: This field stores the URL of the news article's source. It's a `URLField`, ensuring that only valid URLs can be stored.

5. **Category**: This field stores the category assigned to the news article. It's a `CharField` with a maximum length of 50 characters. It's nullable and blank, allowing for articles to be initially stored without a category and later categorized.

6. **sentiment_score**: This field stores the sentiment score of the news article. It's a `FloatField` with a default value of 0.0, indicating a neutral sentiment. This field can be updated with sentiment analysis results if desired.



## Logic and Design Choices
The `classify_news_categories` function in your `tentiems/tasks.py` file performs sentiment analysis on combined text and assigns a category to a news article based on its sentiment score. Here's a breakdown of the implemented logic:

1. **Import Statements**: The necessary imports are made, including `shared_task` from Celery, `NewsArticle` model from your Django app, and `SentimentIntensityAnalyzer` from NLTK.

2. **Download NLTK Resource**: Before the task, the VADER lexicon resource from NLTK is downloaded using `nltk.download('vader_lexicon')`.

3. **classify_news_categories Function**:
   - **Input Parameters**: The function takes `combined_text` (the text to perform sentiment analysis on) and `article_id` (the ID of the news article to update).
   
   - **Sentiment Analysis**: A `SentimentIntensityAnalyzer` object `sid` is initialized. Sentiment analysis is then performed on the combined text using `sid.polarity_scores(combined_text)`, which returns a dictionary containing sentiment scores.
   
   - **Category Assignment**: Based on the sentiment score (specifically the compound score), the function determines the category for the news article. If the compound score is greater than or equal to 0.05, it's categorized as "Positive/Uplifting". If the compound score is less than or equal to -0.05, it's categorized as "Terrorism/Protest/Political Unrest/Riot". Otherwise, it's categorized as "Others".
   
   - **Update Database**: The category determined above is assigned to the corresponding `NewsArticle` object retrieved using the provided `article_id`. The `article.category` field is updated, and changes are saved to the database using `article.save()`.

Overall, this function efficiently analyzes the sentiment of news articles and updates their categories accordingly in the database, providing a crucial step in the automated categorization process.

## Resulting Data
You can retrieve the resulting data in CSV format by accessing the "/export" page after running the server.


## Contributors
- [Aditya Kumar](link_to_your_profile)
