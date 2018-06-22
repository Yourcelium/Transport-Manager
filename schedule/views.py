import operator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.http import JsonResponse
from django.db.models import Q, QuerySet
from django.core.exceptions import ObjectDoesNotExist

from datetime import timezone, datetime, timedelta
from functools import reduce

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Trip, Resident, Destination, MedicalProvider, Issue
from .forms import TripForm, ResidentForm, DestinationForm, MedicalProviderFrom, ResidentSelectForm, IssueForm, TransportationProviderSelectForm
from .serializers import TripSerializer, ResidentSerializer, DestinationSerializer, MedicalProviderSerializer, IssueSerializer 


def dashboard(request):
    return render(request, 'schedule/dashboard.html')

#TRIP
def detail_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'schedule/trip/detail_trip.html', {'trip':trip})

def trip_complete_render(request, pk):
    return render(request, 'schedule/trip/vue/trip_complete.html', {'tripID':pk})




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
    
def pull_triplist_unscheduled_resident(request):
    form = ResidentSelectForm()
    query_param = request.GET.get('resident')
    if query_param:
        trips = Trip.objects.filter(trip_scheduled_status=False, resident=query_param)
        return render(request, 'schedule/trip/list_trips.html', {'trips':trips, 'title':f'All Unscheduled Trips for {query_param}'})
    else:
        return render(request, 'schedule/trip/r_select.html', {'form': form})

def render_unscheduled_triplist(request):
    return render(request, 'schedule/trip/vue/unscheduled.html')


@api_view(['GET'])
def api_get_trip(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    trip = TripSerializer(trip)
    return Response(trip.data)
 

@api_view(['GET'])
def list_today_trips(request):
    floor = int(request.GET.get('floor', 0))
    if floor == 0:
        trips = Trip.objects.filter(appointment_datetime__date=datetime.today())
        trips = TripSerializer(trips, many=True)
        return Response(trips.data)
    else:
        residents = Resident.objects.filter(room_number__startswith=floor)
        residents = [Q(resident=resident) for resident in residents]
        trips = Trip.objects.filter(reduce(operator.or_, residents), appointment_datetime__date=datetime.today()).order_by('-trip_datetime')
        trips = TripSerializer(trips, many=True)
        return Response(trips.data)

@api_view(['GET'])
def list_future_trips(request):
    floor = int(request.GET.get('floor', 0))
    days = int(request.GET.get('days', 7))    
    end = datetime.today() + timedelta(days=days)
    print(datetime.today())
    print(end)
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    print(tomorrow)
    if floor == 0:
        trips = Trip.objects.filter(appointment_datetime__date__gte=tomorrow, appointment_datetime__date__lte=end).order_by('-appointment_datetime')
        print(trips)
        trips = TripSerializer(trips, many=True)
        return Response(trips.data)
    else:    
        residents = Resident.objects.filter(room_number__startswith=floor)
        residents = [Q(resident=resident) for resident in residents]
        trips = Trip.objects.filter(reduce(operator.or_, residents), appointment_datetime__date__gte=tomorrow, appointment_datetime__date__lte=end).order_by('-appointment_datetime')
        trips = TripSerializer(trips, many=True)
        return Response(trips.data)

@api_view(['GET'])
def api_trip_list(request):
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    timerange = request.GET.get('timerange')
    tomorrow_midnight = tomorrow + timedelta(days=1)
    week = tomorrow + timedelta(days=6)
    print(timerange)

    if timerange =='today':
        trips = Trip.objects.filter(appointment_datetime__gte=datetime.now(), appointment_datetime__date__lte=tomorrow)
    elif timerange =='tomorrow':
        trips = Trip.objects.filter(appointment_datetime__gte=tomorrow, appointment_datetime__date__lte=tomorrow_midnight)
    elif timerange == 'week':
        trips = Trip.objects.filter(appointment_datetime__gte=tomorrow_midnight, appointment_datetime__date__lte=week)
    elif timerange == 'week_plus':
        trips = Trip.objects.filter(appointment_datetime__gte=week)
    
    floor = request.GET.get('floor')
    if floor != 0:
        trips = trips.filter(resident__room_number__startswith = floor)
    
    trips = TripSerializer(trips, many=True)
    return Response(trips.data)

def render_trip_request(request):
    return render(request, 'schedule/trip/vue/trip_request.html')


@api_view(['GET'])
def resident_search(request):
    first_name= request.GET.get('first_name')
    last_name= request.GET.get('last_name')
    DOB = request.GET.get('DOB')
    DOB = datetime.strptime(DOB, '%m-%d-%Y')
    try:
        resident = Resident.objects.get(first_name=first_name, last_name=last_name, date_of_birth=DOB)
        resident = ResidentSerializer(resident)
        return Response(resident.data)
    except:
        message = "The form has errors"
        explanation = form.errors.as_data()
        status_code = 400
        return JsonResponse({'message':message,'explanation':explanation}, status=status_code)


@api_view(['POST'])
def destination_create(request):
    form = DestinationForm(request.POST)
    if form.is_valid():
        form.save()
        destination = get_object_or_404(Destination, name=request.POST.get('name'), address=request.POST.get('address') )
        destination = DestinationSerializer(destination)
        return Response(destination.data)
    else:
        return Response(form.errors)

#DESTINATION
@api_view(['GET'])
def destination_list(request):
    destinations = Destination.objects.all()
    destinations = DestinationSerializer(destinations, many=True)
    return Response(destinations.data)  


@api_view(['GET'])
def destination_get(request):
    pk = request.GET.get('id')
    destination = get_object_or_404(Destination, pk=pk)
    destination = DestinationSerializer(destination)
    return Response(destination.data)

@api_view(['POST'])
def trip_complete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    date = trip.appointment_datetime
    date.replace(hour=0, minute=0, second=0, microsecond=0)
    import pdb; pdb.set_trace()
    pick_up_time = request.POST.get('pick_up_time')
    return_time = request.POST.get('return_time')
    
    trip.transport_provider = request.POST.get('transport_provider')
    trip.requestID = request.POST.get('requestID')
    trip.notes = request.POST.get('notes')
    import pdb; pdb.set_trace()

@api_view(['POST'])
def trip_request_create(request):
    resident = get_object_or_404(Resident, pk=request.POST.get('resident'))
    destination = get_object_or_404(Destination, pk=request.POST.get('destination'))
    appointment_datetime = request.POST.get('appointment_datetime')
    appointment_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M')
    import pdb; pdb.set_trace()
    procedure = request.POST.get('procedure')
    strecher = request.POST.get('strecher')
    if strecher == 'false':
        strecher = False
    else:
        strecher = True
    oxygen = request.POST.get('oxygen')
    if oxygen == 'false':
        oxygen = False
    else:
        oxygen = True
    oxygen_liters = request.POST.get('oxygen_liters')
    door_to_door = request.POST.get('door_too_door')
    if door_to_door == 'false':
        door_to_door = False
    else:
        door_to_door = True
    trip = Trip.objects.create(resident=resident, destination=destination, appointment_datetime=appointment_datetime, procedure=procedure, strecher=strecher, oxygen=oxygen, oxygen_liters=oxygen_liters, arranged_by=request.user)
    trip = TripSerializer(trip)
    return Response(trip.data)
    

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
        return render(request, 'schedule/resident/create.html', {'form': form, 'action': 'complete'})

            
    else:
        form = ResidentForm()
        return render(request, 'schedule/resident/create.html', {'form': form, 'action': 'create'})

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


#ISSUES    
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


