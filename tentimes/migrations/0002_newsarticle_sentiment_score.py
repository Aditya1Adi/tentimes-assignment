# Generated by Django 5.0.1 on 2024-01-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tentimes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='sentiment_score',
            field=models.FloatField(default=0.0),
        ),
    ]
