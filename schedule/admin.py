from django.contrib import admin
from .models import Resident, Destination, Trip, MedicalProvider, Issue

admin.site.register(Trip)
admin.site.register(Destination)
admin.site.register(Resident)
admin.site.register(MedicalProvider)
admin.site.register(Issue)

