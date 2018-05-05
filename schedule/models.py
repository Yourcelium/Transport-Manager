from django.db import models
from django.contrib.auth.models import User

class Resident(models.Model):
    first_name=models.CharField(max_length=35)
    last_name=models.CharField(max_length=35)
    date_of_birth = models.DateField()
    medicaid_number = models.CharField(max_length=8, blank=True, null=True)
    room_number = models.CharField(max_length=5, blank=True, null=True)
    ride_to_care_eligble = models.BooleanField(default=False)
    can_transfer = models.BooleanField(default=False)
    wheelchair_van = models.BooleanField(default=True)
    bariatric = models.BooleanField(default=False)
    wheechair_size = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.date_of_birth.strftime("%m/%d/%Y")})'
    
class Destination(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    suite = models.CharField(max_length=20, blank=True, null=True)
    stretcher = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name} at {self.address}'

class MedicalProvider(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    destinations = models.ManyToManyField(Destination, related_name = 'medical_providers', blank=True)
    residents = models.ManyToManyField(Resident, related_name = 'medical_providers', blank=True)
    def __str__(self):
        return '{self.name}'
    

class Trip(models.Model):
    arranged_by = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE) 
    TRANSPORT_PROVIDERS = (
        ('M', 'Metro West'),
        ('R', 'Ride to Care'),
        ('T', 'Trimet Lift'),
        ('F', 'Family/Friend'),
        ('C', 'Cab')
    )
    transport_provider = models.CharField(max_length=1, choices=TRANSPORT_PROVIDERS)
    
    resident = models.ForeignKey(
        Resident, 
        related_name='residents',
        related_query_name='resident', 
        on_delete=models.CASCADE
        )
    destination = models.ForeignKey(
        Destination,
        related_name='destination',
        on_delete=models.CASCADE
    )
    appointment_datetime = models.DateTimeField()
    trip_datetime = models.DateTimeField()
    return_time = models.DateTimeField()
    will_call = models.BooleanField(default=False)
    wait_and_return = models.BooleanField(default=False)
    strecher = models.BooleanField(default=False)
    oxygen = models.BooleanField(default=False)    
    oxygen_liters = models.IntegerField(blank=True, null=True)
    representative_notified = models.CharField(max_length=40, blank=True, null=True)
    tripID = models.CharField(max_length=40, blank=True, null=True)    
    notes = models.CharField(max_length=200, blank=True, null=True)
    procedure = models.CharField(max_length=200)
    door_to_door = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    trip_scheduled_status = models.BooleanField(default=False)
    
    #TODO find out how to corretcly represent transportation provider 
    def __str__(self):
        return f'{self.resident} going to {self.destination.name} on {self.trip_datetime} with {self.transport_provider}'
    
class Issue(models.Model):
    trip = models.ForeignKey(
        Trip,
        related_name='issues',
        related_query_name='issue',
        on_delete=models.CASCADE
    )
    ISSUES = (
        ('L', 'Late'),
        ('N', 'No Show'),
        ('U', 'Unsafe Behavior'),
        ('W', 'Did not wait')
    )
    issue_type = models.CharField(max_length=1, choices=ISSUES)
    description = models.CharField(max_length=300)
    complaint_filed = models.BooleanField(default=False)
    filed_with = models.CharField(max_length=40, blank=True, null=True)
    filed_at = models.DateTimeField(blank=True, null=True)