from django.urls import path


from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('comment/', views.CommentCreateView.as_view(), name='create-comment'),
    path("<str:event_id>/comments/", views.CommentListAPIView.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)