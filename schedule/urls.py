from django.urls import path
from . import views

app_name = 'schedule'
urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    #Trip Paths

    path('trip/edit/<int:pk>', views.edit_trip, name='edit_trip'),    
    path('trip/detail/<int:pk>', views.detail_trip, name='detail_trip'),
    path('trip/delete/<int:pk>', views.delete_trip, name='delete_trip'),
    path('trip/r_select/', views.pull_triplist_unscheduled_resident, name='pull_triplist_unscheduled_resident'),
    path('trip/today', views.list_today_trips, name='list_today_trips'),
    path('trip/future', views.list_future_trips, name='list_future_trips'),
    path('trip/api_trip_list', views.api_trip_list, name='api_trip_list'),
    path('trip/api_unscheduled', views.render_unscheduled_triplist, name='api_triplist_unscheduled'),
    path('trip/request/create', views.trip_request_create, name='trip_request_create'),
    path('trip/request', views.render_trip_request, name="render_trip_request"),
    path('trip/complete/render/<int:pk>', views.trip_complete_render, name="trip_complete"),
    path('trip/complete/<int:pk>', views.trip_complete, name="trip_complete"),
    path('trip/api/detail/<int:pk>', views.api_get_trip, name='api_get_trip'),

    #Resident
    path('resident/', views.list_residents, name='list_residents'),
    path('resident/create/', views.create_resident, name='create_resident'),
    path('resident/detail/<int:pk>', views.detail_resident, name='detail_resident'),
    path('resident/edit/<int:pk>', views.edit_resident, name='edit_resident'),
    path('resident/search/', views.resident_search, name="resident_search"),

    #Medical Provider
    path('medical_provider/', views.list_medical_provider, name='list_medical_provider'),
    path('medical_provider/create/', views.create_medical_provider, name='create_medical_provider'),
    path('medical_provider/detail/<int:pk>', views.detail_medical_provider, name='detail_medical_provider'),
    path('medical_provider/edit/<int:pk>', views.edit_medical_provider, name='edit_medical_provider'),

    #Destination Paths
    path('destination/create', views.destination_create, name='destination_create'),
    path('destination/list', views.destination_list, name='destination_list'),
    path('destination/get/', views.destination_get, name="destination_get"),

    #Issue Paths
    path('issue/', views.issue_list, name='issue_list'),
    path('issue/list_tp', views.issue_list_tp, name='issue_list_tp'),
    path('issue/create/', views.issue_create, name='issue_create'),
    path('issue/detail/<int:pk>', views.issue_detail, name='issue_detail'),
    path('issue/edit/<int:pk>', views.issue_edit, name='issue_edit'),   
]