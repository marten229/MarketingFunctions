# Generated by Django 5.0.6 on 2024-06-14 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketingFunctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialoffer',
            name='code',
            field=models.CharField(default='N/A', max_length=10, unique=True),
        ),
    ]
