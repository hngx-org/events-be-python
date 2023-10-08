from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.UserView.as_view(), name="user_list"),
    path('user/<str:id>', views.SingleUserView.as_view(),name="user_detail"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('create_group/',views.CreateGroupApiView.as_view(),name='create_group'),
    path('get_user_group/',views.GetUserGroupsApiView.as_view(),name='get_user_group'),
    path('update_group/<int:pk>/',views.UpdateGroupApiView.as_view(),name='update_group')
]