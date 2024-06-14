from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import SpecialOffer, Event
from .functions import update_restaurant_profile
from ReviewFeedbackSystem.models import Bewertung
from ReservationManagement.models import Reservation
from RestaurantManagement.models import Restaurant
from UserManagement.models import User
import matplotlib.pyplot as plt
import io
import urllib, base64
from datetime import date
from .forms import DateRangeForm
import pandas as pd

#@login_required
def create_special_offer_view(request, restaurant_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        discount_rate = request.POST.get('discount_rate')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        terms_conditions = request.POST.get('terms_conditions')
        SpecialOffer.objects.create(
            restaurant_id=restaurant_id, title=title, description=description,
            discount_rate=discount_rate, start_date=start_date, end_date=end_date,
            terms_conditions=terms_conditions)
        update_restaurant_profile(restaurant_id)
    return render(request, 'create_special_offer.html')

#@login_required
def manage_special_offers_view(request, restaurant_id):
    special_offers = SpecialOffer.objects.filter(restaurant_id=restaurant_id)
    return render(request, 'manage_special_offers.html', {'special_offers': special_offers})

#@login_required
def create_event_view(request, restaurant_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        terms_conditions = request.POST.get('terms_conditions')
        Event.objects.create(
            restaurant_id=restaurant_id, title=title, description=description,
            start_date=start_date, end_date=end_date, terms_conditions=terms_conditions)
        update_restaurant_profile(restaurant_id)
    return render(request, 'create_event.html')

#@login_required
def manage_events_view(request, restaurant_id):
    events = Event.objects.filter(restaurant_id=restaurant_id)
    return render(request, 'manage_events.html', {'events': events})


def analyze_customer_data(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    form = DateRangeForm(request.GET or None)
    
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        # Kundendaten sammeln
        reservations = Reservation.objects.filter(restaurant=restaurant, datum__range=[start_date, end_date])
        customer_ids = reservations.values_list('user_id', flat=True).distinct()
        customers = User.objects.filter(id__in=customer_ids, role='customer').distinct()
        
        # Demografische Daten analysieren
        demographics = customers.values_list('birthdate', flat=True)
        ages = [(date.today() - birth_date).days // 365 for birth_date in demographics if birth_date]

        # Buchungshistorie analysieren
        booking_history = reservations.values('datum', 'restaurant_id')

        # Dining Preferences und Feedback analysieren
        reviews = Bewertung.objects.filter(user__in=customers, restaurant=restaurant, created_at__range=[start_date, end_date])
        dining_preferences = reviews.values('anlass')
        feedback = reviews.values('bewertung_gesamt', 'bewertung_service', 'bewertung_essen', 'bewertung_ambiente')

        # Grafiken erstellen
        fig, axes = plt.subplots(3, 3, figsize=(15, 10))
        fig.tight_layout(pad=4.0, w_pad=2.0, h_pad=10.0)
        
        # Altersverteilung
        ax = axes[0, 0]
        if ages:
            ax.hist(ages, bins=10, color='skyblue', edgecolor='black')
        ax.set_title('Demographische Verteilung')
        ax.set_xlabel('Alter')
        ax.set_ylabel('Anzahl an Kunden')

        # Buchungshistorie nach Datum
        df_bookings = pd.DataFrame(list(booking_history))
        ax = axes[0, 1]
        if not df_bookings.empty:
            df_bookings['datum'] = pd.to_datetime(df_bookings['datum'])
            booking_counts = df_bookings.groupby(df_bookings['datum'].dt.to_period('D')).size()
            booking_counts.plot(kind='bar', color='orange', ax=ax)
        ax.set_title('Reservierungsverlauf')
        ax.set_xlabel('Tag')
        ax.set_ylabel('Anzahl der Reservierungen')

        # Dining Preferences
        df_preferences = pd.DataFrame(list(dining_preferences))
        ax = axes[0, 2]
        if not df_preferences.empty:
            dining_counts = df_preferences['anlass'].value_counts()
            dining_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_title('Essgewohnheiten')

        # Feedback: Gesamtbewertung
        df_feedback = pd.DataFrame(list(feedback))
        ax = axes[1, 0]
        if not df_feedback.empty:
            gesamt_counts = df_feedback['bewertung_gesamt'].value_counts().sort_index()
            gesamt_counts.plot(kind='bar', color='green', ax=ax)
        ax.set_title('Gesamtbewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        # Feedback: Service
        ax = axes[1, 1]
        if not df_feedback.empty:
            service_counts = df_feedback['bewertung_service'].value_counts().sort_index()
            service_counts.plot(kind='bar', color='red', ax=ax)
        ax.set_title('Servicebewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        # Feedback: Essen
        ax = axes[1, 2]
        if not df_feedback.empty:
            essen_counts = df_feedback['bewertung_essen'].value_counts().sort_index()
            essen_counts.plot(kind='bar', color='blue', ax=ax)
        ax.set_title('Essensbewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        # Feedback: Ambiente
        ax = axes[2, 0]
        if not df_feedback.empty:
            ambiente_counts = df_feedback['bewertung_ambiente'].value_counts().sort_index()
            ambiente_counts.plot(kind='bar', color='yellow', ax=ax)
        ax.set_title('Ambientebewertung')
        ax.set_xlabel('Bewertung')
        ax.set_ylabel('Anzahl')

        # Leere Plots entfernen
        fig.delaxes(axes[2, 1])
        fig.delaxes(axes[2, 2])

        # Grafiken in einem Puffer speichern
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        
        return render(request, 'analyze_customer_data.html', {'data': uri, 'restaurant': restaurant, 'form': form})

    return render(request, 'analyze_customer_data.html', {'form': form, 'restaurant': restaurant})