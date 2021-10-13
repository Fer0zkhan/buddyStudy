from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import *
from .serializers import *


@api_view(['GET'])
def get_rooms_api_view(request):
    rooms = Room.objects.all()
    room_serializer = RoomSerializer(rooms, many=True)
    return Response(room_serializer.data)


@api_view(['GET'])
def get_room_api_view(request, pk):
    room = Room.objects.get(id=pk)
    room_serializer = RoomSerializer(room, many=False)
    return Response(room_serializer.data)
