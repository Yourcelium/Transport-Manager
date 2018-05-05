from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.http import JsonResponse

from datetime import timezone, datetime, timedelta

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Trip, Resident, Destination, MedicalProvider, Issue
from .forms import TripForm, ResidentForm, DestinationForm, MedicalProviderFrom, ResidentSelectForm, IssueForm, TransportationProviderSelectForm
from .serializers import TripSerializer, ResidentSerializer, DestinationSerializer, MedicalProviderSerializer, IssueSerializer 


def dashboard(request):
    return render(request, 'schedule/dashboard.html')

#TRIP
def list_trips(request):
    trips = Trip.objects.all()
    return render(request, 'schedule/trip/list_trips.html', {'trips':trips, 'title':'All Trips'})
    
def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.arranged_by = request.user
            trip.save()
            return redirect('schedule:detail_trip', pk=trip.pk)
    else:
        form = TripForm()
    return render(request, 'schedule/trip/create_trip.html', {'form': form})

def detail_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'schedule/trip/detail_trip.html', {'trip':trip})

def edit_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.arranged_by = request.user
            trip.save()
            return redirect('schedule:view_trip', pk=trip.pk)
    else:
        form = TripForm(instance=trip)
    return render(request, 'schedule/trip/create_trip.html', {'form': form})

def delete_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)    
    if request.methodls == 'POST':
        trip.delete()
        return redirect('schedule:list_trips')



def pull_triplist_unscheduled(request):
    trips = Trip.objects.all().filter(trip_scheduled_status=False)
    return render(request, 'schedule/trip/list_trips.html', {'trips':trips, 'title':'All Unscheduled Trips'})
    

def pull_triplist_unscheduled_transport_provider(request):
    query_param = request.GET.get('transportation_provider')
    if query_param:
        trips = Trip.objects.filter(trip_scheduled_status=False, transport_provider=query_param)
        return render(request, 'schedule/trip/list_trips.html', {'Trip': Trip, 'trips':trips, 'title':f'All Unscheduled {query_param} Trips'})
    else:
        return render(request, 'schedule/trip/tp_select.html', {'Trip': Trip})

def pull_triplist_unscheduled_resident(request):
    form = ResidentSelectForm()
    query_param = request.GET.get('resident')
    if query_param:
        trips = Trip.objects.filter(trip_scheduled_status=False, resident=query_param)
        return render(request, 'schedule/trip/list_trips.html', {'trips':trips, 'title':f'All Unscheduled Trips for {query_param}'})
    else:
        return render(request, 'schedule/trip/r_select.html', {'form': form})

def render_unscheduled_triplist(request):
    return render(request, 'schedule/trip/api_list_trip_unscheduled.html')


# API VIEWS
@api_view(['GET'])
def list_today_trips(request):
    trips = Trip.objects.filter(trip_datetime__date=datetime.today())
    trips = TripSerializer(trips, many=True)
    return Response(trips.data)

@api_view(['GET'])
def list_future_trips(request):
    days = int(request.GET.get('days', 7))
    end = datetime.today() + timedelta(days=days)
    tomorrow = datetime.today() + timedelta(days=1)
    trips = Trip.objects.filter(trip_datetime__date__gte=tomorrow, trip_datetime__date__lte=end)
    trips = TripSerializer(trips, many=True)
    return Response(trips.data)

@api_view(['GET'])
def api_triplist_unscheduled(request):
    days = int(request.GET.get('days', 7))    
    trips = Trip.objects.filter(trip_scheduled_status=False)
    trips = TripSerializer(trips, many=True)
    return Response(trips.data)








#RESIDENT
def list_residents(request):
    residents = Resident.objects.all()
    return render(request, 'schedule/resident/list.html', {'residents':residents})


def create_resident(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            resident = form.save(commit=False)
            resident.save()
    else:
        form = ResidentForm()
    return render(request, 'schedule/resident/create.html', {'form': form})

def detail_resident(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    return render(request, 'schedule/resident/detail.html')

def edit_resident(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            resident = form.save(commit=False)
            trip.save()
            return redirect('schedule:detail_resident', pk=resident.pk)


#Medcial Provider
def list_medical_provider(render):
    if request.method== 'POST':
        residents = MedicalProvider.objects.all()
        return render(request, 'schedule/medical_provider/list.html')

def create_medical_provider(request):
    if request.method == 'POST':
        form = MedicalProviderFrom(request.POST)
        if form.is_valid():
            medical_provider = form.save(commit=False)
            medical_provider.save()
    else:
        form = MedicalProviderFrom()
    return render(request, 'schedule/medical_provider/create.html', {'form': form})

def detail_medical_provider(request, pk):
    medical_provider = get_object_or_404(MedicalProvider, pk=pk)
    return render(request, 'schedule/medical_provider/detail.html')

def edit_medical_provider(request, pk):
    medical_provider = get_object_or_404(MedicalProvider, pk=pk)
    if request.method == 'POST':
        form = MedicalProviderFrom(request.POST, instance=medical_provider)
        if form.is_valid():
            resident = form.save(commit=False)
            trip.save()
            return redirect('detail_medical_provider', pk=medical_provider.pk)


#DESTINATION
class DestinationListView(ListView):
    model = Destination
    template_name = 'schedule/destination/list_destination.html'

class DestinationCreateView(CreateView):
    model = Destination
    template_name = 'schedule/destination/create_destination.html'
    form_class = DestinationForm

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'schedule/destination/detail_destination.html'
    
def issue_create(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return redirect('schedule:issue_detail', pk=issue.pk)
    else:
        form= IssueForm()
    return render(request, 'schedule/issue/create.html', {'form': form})

def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    return render(request, 'schedule/issue/detail.html', {'issue':issue})

def issue_edit(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
            form = IssueForm(request.POST, instance=issue)
            if form.is_valid():
                issue = form.save()
            return redirect('schedule:issue_detail', pk=issue.pk)
    else:
        form = IssueForm(instance=issue)
    return render(request, 'schedule/issue/create.html', {'form': form})

def issue_list(request):
    issues = Issue.objects.all()
    return render (request, 'schedule/issue/list.html', {'issues':issues, 'title':'All Reported Transportation Issues'})

def issue_list_tp(request):
    form = TransportationProviderSelectForm()
    query_param = request.GET.get('transportation_provider')
    if query_param:
        issues = Issue.objects.filter(trip__transport_provider=query_param)
        return render(request, 'schedule/issue/list.html', {'issues':issues, 'title': f'All Issues with {query_param}'})
    else:
        return render(request, 'schedule/issue/tp_select.html', {'form': form})

# def issue_list_resident(request):
#     form = ResidentSelectForm()
#     query_param = request.GET.get('resident')
#     if query_param:
#         issues = Issue.obj

def issue_list_driver(request):
    pass

def issue_list_time(request):
    pass