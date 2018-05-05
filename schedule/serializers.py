from rest_framework import serializers
from .models import Resident, Destination, MedicalProvider, Trip, Issue
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'

class MedicalProviderSerializer(serializers.ModelSerializer):
    destinations = DestinationSerializer(many=True)
    residents = ResidentSerializer(many=True)
    class Meta:
        model = MedicalProvider
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    arranged_by = UserSerializer()
    destination = DestinationSerializer()
    resident = ResidentSerializer()
    class Meta:
        model = Trip
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    trip = TripSerializer()
    class Meta:
        model = Issue
        fields = '__all__'


