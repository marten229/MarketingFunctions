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

