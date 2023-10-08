from django.urls import path
from . import views
from events.views import CalenderView,EventDelView


urlpatterns = [
    path('events/calendar', CalenderView.as_view(), name='calender'),
    path('events/<int:id>',EventDelView.as_view(), name='Delevent')
]