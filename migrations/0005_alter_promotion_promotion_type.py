# Generated by Django 5.0.6 on 2024-06-16 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketingFunctions', '0004_loyaltyprogram_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='promotion_type',
            field=models.CharField(choices=[('discount', 'Rabatt'), ('special_item', 'Gericht außerhalb der Karte')], max_length=20),
        ),
    ]
