from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime, timedelta
from RestaurantManagement.models import Restaurant
from UserManagement.models import User

class SpecialOffer(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='special_offers')
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, default='N/A')
    description = models.TextField()
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    terms_conditions = models.TextField()

class Event(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    terms_conditions = models.TextField()


class Promotion(models.Model):
    DISCOUNT = 'discount'
    SPECIAL_ITEM = 'special_item'
    LOYALTY_POINTS = 'loyalty_points'
    
    PROMOTION_TYPES = [
        (DISCOUNT, 'Rabatt'),
        (SPECIAL_ITEM, 'Gericht außerhalb der Karte'),
        (LOYALTY_POINTS, 'Treuepunkte')
    ]
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='promotions')
    name = models.CharField(max_length=100)
    description = models.TextField()
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

