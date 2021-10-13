from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home-view'),
    path('login/', login_view, name='login-view'),
    path('logout/', logout_view, name='logout-view'),
    path('register/', register_view, name='register-view'),

    path('profile/<str:pk>/', profile_view, name='profile-view'),

    path('room/<str:pk>', room_view, name='room-view'),
    path('create/room/', create_room_view, name='create-room'),
    path('update/room/<str:pk>/', update_room_view, name='update-room'),
    path('delete/room/<str:pk>/', delete_room_view, name='delete-room'),

    path('delete/message/<str:pk>/', delete_message_view, name='delete-message'),
    path('update/user/', update_user_view, name='update-user'),

    path('topics/', topics_view, name='topics-view'),
    path('activity/', activity_view, name='activity-view'),
]
