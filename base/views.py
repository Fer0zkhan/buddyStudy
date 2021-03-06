from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *


# Create your views here.
def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home-view')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exit')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-view')
        else:
            messages.error(request, 'Email and password does not exit')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home-view')


def register_view(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home-view')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'base/login_register.html', context)


def home_view(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages
    }
    return render(request, 'base/home.html', context)


def room_view(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room-view', pk=room.id)
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)


def profile_view(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login-view')
def create_room_view(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home-view')
    context = {
        'form': form,
        'topics': topics
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login-view')
def update_room_view(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home-view')
    context = {
        'form': form,
        'topics': topics,
        'room': room
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login-view')
def delete_room_view(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home-view')
    context = {
        'room': room
    }
    return render(request, 'base/delete_room_form.html', context)


@login_required(login_url='login-view')
def delete_message_view(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home-view')
    context = {
        'obj': message
    }
    return render(request, 'base/delete_room_form.html', context)


@login_required(login_url='login-view')
def update_user_view(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile-view', pk=user.id)
    context = {
        'form': form
    }
    return render(request, 'base/update_user.html', context)


def topics_view(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {
        'topics': topics
    }
    return render(request, 'base/topic.html', context)


def activity_view(request):
    room_messages = Message.objects.all()
    context = {
        'room_messages': room_messages
    }
    return render(request, 'base/activity.html', context)
