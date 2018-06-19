from django.forms.models import ModelForm
from django.forms import Form, ChoiceField
from .models import Trip, Resident, Destination, MedicalProvider, Issue
from django import forms
from django.contrib.admin import widgets

class TripForm(ModelForm):
    resident = forms.ModelChoiceField(queryset=Resident.objects.all())
    clinic = forms.ModelChoiceField(queryset=Destination.objects.all())
    class Meta:
        model = Trip
        exclude = ['created_date, trip_scheduled_status']
        widgets = {
            'trip_time': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
            'return_time': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }

class ResidentForm(ModelForm):
    class Meta:
        model = Resident
        fields = '__all__'

class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'

class MedicalProviderFrom(ModelForm):
    class Meta:
        model = MedicalProvider
        fields = '__all__'

class ResidentSelectForm(Form):
    resident = forms.ModelChoiceField(queryset=Resident.objects.all())
    
class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = '__all__'

class TransportationProviderSelectForm(Form):
    TRANSPORT_PROVIDERS = (
        ('M', 'Metro West'),
        ('R', 'Ride to Care'),
        ('T', 'Trimet Lift'),
        ('F', 'Family/Friend'),
        ('C', 'Cab')
    )
    transportation_provider = forms.ChoiceField(choices=TRANSPORT_PROVIDERS)