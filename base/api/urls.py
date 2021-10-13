from django.urls import path
from .views import *

urlpatterns = [
    path('rooms/', get_rooms_api_view),
    path('rooms/<str:pk>/', get_room_api_view)
]
