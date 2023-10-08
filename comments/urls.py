from django.urls import path


from . import views


urlpatterns = [
    path("api/<str:event_id>/comment", views.create_comment),
]
