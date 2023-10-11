from django.urls import path


from . import views


urlpatterns = [
    path("<str:event_id>/comment/", views.create_comment),
    path("<str:event_id>/comments/", views.CommentListAPIView.as_view()),
]
