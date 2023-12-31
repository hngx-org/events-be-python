from django.urls import path, re_path, include
from users import views


urlpatterns = [
    # path('user/', views.UserView.as_view(), name="user_list"),
    # path('user/<str:id>/', views.SingleUserView.as_view(),name="user_detail"),
    # path('auth/google/login/', views.GoogleLoginView.as_view(), name='google-login'),
    # path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    # path('login/', views.newLoginView.as_view(), name='login'),
    # path('auth/', views.AuthView.as_view(), name='auth'),
    # path('user/', views.sendNotification.as_view(), name='send-notification'),
    # path('edit-user-group/<int:pk>/', views.editUserGroup.as_view(), name='edit-user-group'),

    path('profile/', views.UserProfileView.as_view(), name='login'),
    path('group/',views.CreateGroupApiView.as_view(),name='create_group'),
    path('group/<int:pk>/update/',views.UpdateGroupApiView.as_view(),name='update_group'),
    path('group/<int:pk>/delete/',views.DeleteGroupApiView.as_view(),name='delete_group'),
    path('group/<int:pk>/',views.RetrieveGroupApiView.as_view(),name='retrieve_group'),
    path('user_groups/',views.GetUserGroupsApiView.as_view(),name='get_user_group'),
    path('user_groups/detail',views.GetUserGroupDetail.as_view(),name='get_user_group_detail'),
    path('groups/add_friend/<int:group_id>/', views.AddFriendToGroup.as_view(), name='add_friend_to_group'),
    path('user/<str:email>/',views.GetUserDetailViews.as_view(),name='get_user_detail'),
    path('settings/appearance/',views.AppearanceSetting.as_view(),name='set_appearance'),
    path('settings/languageregion/',views.LanguageRegionSettings.as_view(),name='set_language'),
    path('notifications/<int:pk>/', views.SingleNotificationView.as_view(), name='single-notification'),
    path('notifications/', views.AllNotificationsView.as_view(), name='all-notifications'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us')

]