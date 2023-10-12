from django.urls import path, re_path, include
from users import views


urlpatterns = [
    # path('user/', views.UserView.as_view(), name="user_list"),
    # path('user/<str:id>/', views.SingleUserView.as_view(),name="user_detail"),
    
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),

    path('profile/', views.UserProfileView.as_view(), name='login'),
    # path('login/', views.newLoginView.as_view(), name='login'),
    # path('auth/', views.AuthView.as_view(), name='auth'),
    path('group/',views.CreateGroupApiView.as_view(),name='create_group'),
    path('group/<int:pk>/update/',views.UpdateGroupApiView.as_view(),name='update_group'),
    path('group/<int:pk>/delete/',views.DeleteGroupApiView.as_view(),name='delete_group'),
    path('group/<int:pk>/',views.RetrieveGroupApiView.as_view(),name='retrieve_group'),
    path('user_groups/',views.GetUserGroupsApiView.as_view(),name='get_user_group'),
    path('user_groups/detail',views.GetUserGroupDetail.as_view(),name='get_user_group_detail'),
    path('groups/add_friend/<int:group_id>/', views.AddFriendToGroup.as_view(), name='add_friend_to_group'),
    # path('edit-user-group/<int:pk>/', views.editUserGroup.as_view(), name='edit-user-group'),

]