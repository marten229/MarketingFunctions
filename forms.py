from django import forms
from .models import SpecialOffer, Event, Promotion

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


from django import forms
from .models import Promotion

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['name', 'description', 'promotion_type', 'value', 'active']
        labels = {
            'name': 'Name',
            'description': 'Beschreibung',
            'promotion_type': 'Art der Promotion',
            'value': 'Wert',
            'active': 'Aktiv',
        }


