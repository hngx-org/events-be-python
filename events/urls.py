from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    #Define URL patterns for your views
    path('events/', views.CreateEventView.as_view(), name='create-event'),
    path('events/all/', views.EventsView.as_view(), name='events-list'),
    path('events/<str:event_id>/', views.getEvent.as_view(), name='event-detail'),
    path('events/search/<str:keyword>/', views.SearchEventView.as_view(), name='event-search'),
    path('events/<uuid:event_uuid>/update/', views.UpdateEventView.as_view(), name='event-update'),
    path('events/calendar', views.CalenderView.as_view(), name='calender'),
    path('events/<str:id>/delete',views.EventDelView.as_view(), name='Delevent'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
