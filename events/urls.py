from django.urls import path
from . import views




urlpatterns = [
    #Define URL patterns for your views
    path('events/', views.CreateEventView.as_view(), name='create-event'),
    path('events/all/', views.EventsView.as_view(), name='events-list'),
    path('events/<str:event_id>/', views.getEvent.as_view(), name='event-detail'),
    path('events/search/<str:keyword>/', views.SearchEventView.as_view(), name='event-search'),
    path('events/<uuid:event_uuid>/update/', views.UpdateEventView.as_view(), name='event-update'),
    path('events/calendar', views.CalenderView.as_view(), name='calender'),
    path('events/<str:id>/delete',views.EventDelView.as_view(), name='Delevent'),
    path('events/<str:event_id>/join/', views.JoinEvent.as_view(), name='join-event'),
    path('<str:group_id>/events/', views.getGroupEvents.as_view(), name='join-event'),
    path('friends_events/',views.OtherUserGroupEvents.as_view(),name='friends_events'),
    path('events/<str:event_id>/leave/', views.LeaveEvent.as_view(), name='leave-event'),
]
