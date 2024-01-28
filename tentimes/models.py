from django.db import models

# Create your models here.

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField()
    source_url = models.URLField()
    category = models.CharField(max_length=50, null=True, blank=True)
    sentiment_score = models.FloatField(default=0.0)  #

