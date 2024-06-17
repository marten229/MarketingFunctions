from django.test import TestCase, Client
from django.urls import reverse
from UserManagement.models import User
from django.contrib.auth.models import Group
from .models import SpecialOffer, Event, Promotion
from RestaurantManagement.models import Restaurant

class SpecialOfferViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.groups.add(Group.objects.get_or_create(name='restaurant_owner')[0])
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.client.login(username='testuser', password='12345')

    def test_create_special_offer_view(self):
        response = self.client.post(reverse('create_special_offer', args=[self.restaurant.pk]), {
            'title': 'Test Offer',
            'description': 'Test Description',
            'discount_rate': 10,
            'code': 'TEST10',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'terms_conditions': 'Test Terms'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SpecialOffer.objects.count(), 1)
        self.assertEqual(SpecialOffer.objects.first().title, 'Test Offer')

    def test_manage_special_offers_view(self):
        SpecialOffer.objects.create(restaurant=self.restaurant, title='Test Offer', code='TEST10', description='Test Description', discount_rate=10, start_date='2023-01-01', end_date='2023-12-31', terms_conditions='Test Terms')
        response = self.client.get(reverse('manage_special_offers', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_special_offers.html')
        self.assertContains(response, 'Test Offer')

    def test_delete_special_offer_view(self):
        special_offer = SpecialOffer.objects.create(restaurant=self.restaurant, title='Test Offer', code='TEST10', description='Test Description', discount_rate=10, start_date='2023-01-01', end_date='2023-12-31', terms_conditions='Test Terms')
        response = self.client.post(reverse('delete_special_offer', args=[self.restaurant.pk, special_offer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SpecialOffer.objects.count(), 0)

class EventViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.groups.add(Group.objects.get_or_create(name='restaurant_owner')[0])
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.client.login(username='testuser', password='12345')

    def test_create_event_view(self):
        response = self.client.post(reverse('create_event', args=[self.restaurant.pk]), {
            'title': 'Test Event',
            'description': 'Test Description',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'terms_conditions': 'Test Terms'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().title, 'Test Event')

    def test_manage_events_view(self):
        Event.objects.create(restaurant=self.restaurant, title='Test Event', description='Test Description', start_date='2023-01-01', end_date='2023-12-31', terms_conditions='Test Terms')
        response = self.client.get(reverse('manage_events', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_events.html')
        self.assertContains(response, 'Test Event')

    def test_delete_event_view(self):
        event = Event.objects.create(restaurant=self.restaurant, title='Test Event', description='Test Description', start_date='2023-01-01', end_date='2023-12-31', terms_conditions='Test Terms')
        response = self.client.post(reverse('delete_event', args=[self.restaurant.pk, event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 0)

class PromotionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.groups.add(Group.objects.get_or_create(name='restaurant_owner')[0])
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.client.login(username='testuser', password='12345')

    def test_create_promotion_view(self):
        response = self.client.post(reverse('create_promotion', args=[self.restaurant.pk]), {
            'name': 'Test Promotion',
            'description': 'Test Description',
            'promotion_type': 'discount',
            'value': 20,
            'active': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Promotion.objects.count(), 1)
        self.assertEqual(Promotion.objects.first().name, 'Test Promotion')

    def test_manage_promotions_view(self):
        Promotion.objects.create(restaurant=self.restaurant, name='Test Promotion', description='Test Description', promotion_type='discount', value=20, active=True)
        response = self.client.get(reverse('manage_promotions', args=[self.restaurant.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_promotions.html')
        self.assertContains(response, 'Test Promotion')

    def test_delete_promotion_view(self):
        promotion = Promotion.objects.create(restaurant=self.restaurant, name='Test Promotion', description='Test Description', promotion_type='discount', value=20, active=True)
        response = self.client.post(reverse('delete_promotion', args=[self.restaurant.pk, promotion.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Promotion.objects.count(), 0)
