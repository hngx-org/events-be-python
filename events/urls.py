from django.urls import path
from . import views




urlpatterns = [
    path('events/get/', views.EventsView.as_view(),name="Get_Events"),


    path('events/<str:event_id>/', views.update_event, name='update_event'),
]
