from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Startdatum')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Enddatum')
