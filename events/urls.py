from django.urls import path
from . import views

urlpatterns = [
    path('/api/events', views.EventsView.as_view()),
    path('/api/events/<uuid:event_id>', views.getEvent.as_view(), name="get-event-by-id"),
    path('/api/events/search/<str:keyword>', views.SearchEventView.as_view(), name="search-event")
]
