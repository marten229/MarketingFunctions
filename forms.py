from django import forms
from .models import SpecialOffer, Event

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Startdatum')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Enddatum')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'terms_conditions']

class SpecialOfferForm(forms.ModelForm):
    class Meta:
        model = SpecialOffer
        fields = ['title', 'description', 'discount_rate', 'start_date', 'end_date', 'terms_conditions']
