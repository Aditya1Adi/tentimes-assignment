from django.shortcuts import render
from tentimes.models import NewsArticle
import csv
from django.http import HttpResponse
from .tasks import classify_news_categories


def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['title', 'content', 'pub_date','source_url','category'])  # Write headers

    queryset = NewsArticle.objects.all()  # Replace YourModel with your actual model
    for obj in queryset:
        writer.writerow([obj.title,obj.content,obj.pub_date,obj.source_url,obj.category])  # Write data

    return response


def news_list(request):
    # Retrieve all news articles from the database
    articles = NewsArticle.objects.all()
    
    for article in articles:
        # Combine title and content
        combined_text = article.title + " " + article.content
        
        # Perform sentiment analysis and categorization
        classify_news_categories(combined_text, article.id)
    # articles = NewsArticle.objects.all()
    return render(request, 'tentimes/home.html', {'articles': articles})


