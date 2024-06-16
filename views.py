from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SpecialOffer, Event, Promotion
from ReviewFeedbackSystem.models import Bewertung
from ReservationManagement.models import Reservation
from RestaurantManagement.models import Restaurant, MenuItem
from UserManagement.models import User
import matplotlib.pyplot as plt
import io
import urllib, base64
from datetime import date
from .forms import DateRangeForm
import pandas as pd
from .forms import SpecialOfferForm, EventForm, PromotionForm
from django.contrib.auth.decorators import login_required
from UserManagement.decorators import role_and_restaurant_required

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def create_special_offer_view(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = SpecialOfferForm(request.POST)
        if form.is_valid():
            special_offer = form.save(commit=False)
            special_offer.restaurant = restaurant
            special_offer.save()
            return redirect('manage_special_offers', pk=pk)
    else:
        form = SpecialOfferForm()
    return render(request, 'create_special_offer.html', {'form': form, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def manage_special_offers_view(request, pk):
    special_offers = SpecialOffer.objects.filter(restaurant_id=pk)
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'manage_special_offers.html', {'special_offers': special_offers, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def delete_special_offer_view(request, pk, special_offer_id):
    special_offer = get_object_or_404(SpecialOffer, id=special_offer_id)
    pk = special_offer.restaurant_id
    special_offer.delete()
    return redirect('manage_special_offers', pk=pk)

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def create_event_view(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.restaurant = restaurant
            event.save()
            return redirect('manage_events', pk=pk)
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def manage_events_view(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    events = Event.objects.filter(restaurant_id=pk)
    return render(request, 'manage_events.html', {'events': events, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def delete_event_view(request, pk, event_id):
    event = get_object_or_404(Event, id=event_id)
    pk = event.restaurant_id
    event.delete()
    return redirect('manage_events', pk=pk)

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def analyze_customer_data(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = DateRangeForm(request.GET or None)
    
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        reservations = Reservation.objects.filter(restaurant=restaurant, datum__range=[start_date, end_date])
        customer_ids = reservations.values_list('user_id', flat=True).distinct()
        customers = User.objects.filter(id__in=customer_ids, role='customer').distinct()
        
        demographics = customers.values_list('birthdate', flat=True)
        ages = [(date.today() - birth_date).days // 365 for birth_date in demographics if birth_date]

        booking_history = reservations.values('datum', 'uhrzeit', 'restaurant_id')

        reviews = Bewertung.objects.filter(user__in=customers, restaurant=restaurant, created_at__range=[start_date, end_date])
        dining_preferences = reviews.values('anlass')
        feedback = reviews.values('bewertung_gesamt', 'bewertung_service', 'bewertung_essen', 'bewertung_ambiente')

        menu_items = MenuItem.objects.filter(restaurant=restaurant)
        reservations_with_dishes = reservations.prefetch_related('gerichte')
        
        dish_counts = {}
        for reservation in reservations_with_dishes:
            for dish in reservation.gerichte.all():
                if dish.name in dish_counts:
                    dish_counts[dish.name] += 1
                else:
                    dish_counts[dish.name] = 1

        fig, axes = plt.subplots(5, 3, figsize=(15, 18))
        fig.tight_layout(pad=4.0, w_pad=2.0, h_pad=10.0)
        
        ax = axes[0, 0]
        if ages:
            ax.hist(ages, bins=10, color='skyblue', edgecolor='black')
        ax.set_title('Demographische Verteilung')
        ax.set_xlabel('Alter')
        ax.set_ylabel('Anzahl an Kunden')

        df_bookings = pd.DataFrame(list(booking_history))
        ax = axes[0, 1]
        if not df_bookings.empty:
            df_bookings['datum'] = pd.to_datetime(df_bookings['datum'])
            booking_counts = df_bookings.groupby(df_bookings['datum'].dt.to_period('D')).size()
            booking_counts.plot(kind='bar', color='orange', ax=ax)
        ax.set_title('Reservierungsverlauf')
        ax.set_xlabel('Tag')
        ax.set_ylabel('Anzahl der Reservierungen')

        ax = axes[0, 2]
        if not df_bookings.empty:
            df_bookings['monat'] = df_bookings['datum'].dt.to_period('M')
            season_counts = df_bookings['monat'].value_counts().sort_index()
            season_counts.plot(kind='bar', color='teal', ax=ax)
        ax.set_title('Reservierungen nach Monat')
        ax.set_xlabel('Monat')
        ax.set_ylabel('Anzahl der Reservierungen')

        ax = axes[1, 0]
        if not df_bookings.empty:
            df_bookings['uhrzeit'] = pd.to_datetime(df_bookings['uhrzeit'], format='%H:%M:%S').dt.hour
            time_counts = df_bookings['uhrzeit'].value_counts().sort_index()
            time_counts.plot(kind='bar', color='purple', ax=ax)
        ax.set_title('Reservierungen nach Uhrzeit')
        ax.set_xlabel('Uhrzeit')
        ax.set_ylabel('Anzahl der Reservierungen')

        df_preferences = pd.DataFrame(list(dining_preferences))
        ax = axes[1, 1]
        if not df_preferences.empty:
            dining_counts = df_preferences['anlass'].value_counts()
            dining_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Essgewohnheiten')

        ax = axes[1, 2]
        if dish_counts:
            dishes = pd.Series(dish_counts)
            dishes.sort_values(ascending=False).plot(kind='bar', color='brown', ax=ax)
        ax.set_title('Am meisten ausgewählte Gerichte')
        ax.set_xlabel('Gericht')
        ax.set_ylabel('Anzahl der Auswahl')

        df_feedback = pd.DataFrame(list(feedback))
        ax = axes[2, 0]
        if not df_feedback.empty:
            gesamt_counts = df_feedback['bewertung_gesamt'].value_counts().sort_index()
            gesamt_counts.plot(kind='bar', color='green', ax=ax)
        ax.set_title('Gesamtbewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        ax = axes[2, 1]
        if not df_feedback.empty:
            service_counts = df_feedback['bewertung_service'].value_counts().sort_index()
            service_counts.plot(kind='bar', color='red', ax=ax)
        ax.set_title('Servicebewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        ax = axes[2, 2]
        if not df_feedback.empty:
            essen_counts = df_feedback['bewertung_essen'].value_counts().sort_index()
            essen_counts.plot(kind='bar', color='blue', ax=ax)
        ax.set_title('Essensbewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        ax = axes[3, 0]
        if not df_feedback.empty:
            ambiente_counts = df_feedback['bewertung_ambiente'].value_counts().sort_index()
            ambiente_counts.plot(kind='bar', color='yellow', ax=ax)
        ax.set_title('Ambientebewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        fig.delaxes(axes[3, 1])
        fig.delaxes(axes[3, 2])
        fig.delaxes(axes[4, 0])
        fig.delaxes(axes[4, 1])
        fig.delaxes(axes[4, 2])

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        
        return render(request, 'analyze_customer_data.html', {'data': uri, 'restaurant': restaurant, 'form': form})

    return render(request, 'analyze_customer_data.html', {'form': form, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def create_promotion_view(request, pk):
    restaurant = get_object_or_404(Restaurant, id=pk)
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.restaurant = restaurant
            promotion.save()
            return redirect('manage_promotions', pk=restaurant.id)
    else:
        form = PromotionForm()
    return render(request, 'create_promotion.html', {'form': form, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def manage_promotions_view(request, pk):
    restaurant = get_object_or_404(Restaurant, id=pk)
    promotions = Promotion.objects.filter(restaurant=restaurant)
    return render(request, 'manage_promotions.html', {'promotions': promotions, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def delete_promotion_view(request, pk, promotion_id):
    promotion = get_object_or_404(Promotion, id=promotion_id)
    restaurant_id = promotion.restaurant.id
    promotion.delete()
    return redirect('manage_promotions', pk=restaurant_id)