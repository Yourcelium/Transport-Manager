from django.urls import path
from . import views

app_name = 'schedule'
urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    #Trip Paths
    # path('trip/', views.home, name='home'),
    path('trip/', views.list_trips, name='list_trips' ),    
    path('trip/create/', views.create_trip, name='create_trip'),
    path('trip/edit/<int:pk>', views.edit_trip, name='edit_trip'),    
    path('trip/detail/<int:pk>', views.detail_trip, name='detail_trip'),
    path('trip/delete/<int:pk>', views.delete_trip, name='delete_trip'),
    path('trip/unscheduled/', views.pull_triplist_unscheduled, name='pull_triplist_unscheduled'),
    path('trip/tp_select/', views.pull_triplist_unscheduled_transport_provider, name='pull_triplist_unscheduled_transport_provider'),
    path('trip/r_select/', views.pull_triplist_unscheduled_resident, name='pull_triplist_unscheduled_resident'),
    path('trip/today', views.list_today_trips, name='list_today_trips'),
    path('trip/future', views.list_future_trips, name='list_future_trips'),
    path('trip/api_triplist_unscheduled', views.api_triplist_unscheduled, name='api_triplist_unscheduled'),
    path('trip/api_unscheduled', views.render_unscheduled_triplist, name='api_triplist_unscheduled'),


    #Resident
    path('resident/', views.list_residents, name='list_residents'),
    path('resident/create/', views.create_resident, name='create_resident'),
    path('resident/detail/<int:pk>', views.detail_resident, name='detail_resident'),
    path('resident/edit/<int:pk>', views.edit_resident, name='edit_resident'),

    #Medical Provider
    path('medical_provider/', views.list_medical_provider, name='list_medical_provider'),
    path('medical_provider/create/', views.create_medical_provider, name='create_medical_provider'),
    path('medical_provider/detail/<int:pk>', views.detail_medical_provider, name='detail_medical_provider'),
    path('medical_provider/edit/<int:pk>', views.edit_medical_provider, name='edit_medical_provider'),

    #Destination Paths
    path('destination/', views.DestinationListView.as_view(), name='list_destination'),

    #Issue Paths
    path('issue/', views.issue_list, name='issue_list'),
    path('issue/list_tp', views.issue_list_tp, name='issue_list_tp'),
    path('issue/create/', views.issue_create, name='issue_create'),
    path('issue/detail/<int:pk>', views.issue_detail, name='issue_detail'),
    path('issue/edit/<int:pk>', views.issue_edit, name='issue_edit'),   
]