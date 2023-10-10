from django.urls import path
from users import views


urlpatterns = [
    path('user/', views.UserView.as_view(), name="user_list"),
    path('user/<str:id>/', views.SingleUserView.as_view(),name="user_detail"),
    #path('login/', views.LoginView.as_view(), name='login'),
    path('login/', views.newLoginView.as_view(), name='login'),
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('group/',views.CreateGroupApiView.as_view(),name='create_group'),
    path('group/<int:pk>/update/',views.UpdateGroupApiView.as_view(),name='update_group'),
    path('group/<int:pk>/delete/',views.DeleteGroupApiView.as_view(),name='delete_group'),
    path('group/<int:pk>/',views.RetrieveGroupApiView.as_view(),name='retrieve_group'),
    path('user_groups/',views.GetUserGroupsApiView,name='get_user_group'),
    # path('edit-user-group/<int:pk>/', views.editUserGroup.as_view(), name='edit-user-group'),

]