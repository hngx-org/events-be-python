from django.urls import path
from . import views




urlpatterns = [
    # Define URL patterns for your views
    path('events/', views.CreateEventView.as_view(), name='create-event'),
    path('events/', views.EventsView.as_view(), name='events-list'),
    path('events/<int:event_id>/', views.getEvent.as_view(), name='event-detail'),
    path('events/search/', views.SearchEventView.as_view(), name='event-search'),
    path('events/<int:event_id>/update/', views.update_event, name='event-update'),
]
