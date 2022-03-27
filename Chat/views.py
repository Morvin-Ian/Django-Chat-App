from email import message
from multiprocessing import context
from urllib.request import Request
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import ChatRoom, Topic, Message
from .forms import RoomForm, UpdateDetails, UpdateProfile, UserRegistrationForm


@login_required(login_url='login')
def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
   
    rooms = ChatRoom.objects.filter(
        Q(room_title__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    
    ) # Accessing foreign-keyed values upwards
    comments = Message.objects.all()
    topics = Topic.objects.all()

    p = Paginator(ChatRoom.objects.all(), 2)
    page = request.GET.get('page')
    room = p.get_page(page)

    context = {"rooms":rooms, "topics":topics, "comments":comments,"room":room}
    return render(request, 'Chat/index.html', context)

@login_required(login_url='login')
def room_view(request, pk):
    room = ChatRoom.objects.get(id=pk)
    comments = room.message_set.all() 
    participants = room.room_members.all()
    print(comments)

    if request.method == 'POST':
        comment = Message.objects.create(
            user = request.user,
            room=room,
            body = request.POST.get('comment'))
        room.room_members.add(request.user)
        return redirect('room-page', pk=room.id)

    context = {
        "comments":comments,
        "room":room, 
        "participants":participants
    }
 

    return render(request, 'Chat/room.html', context)

@login_required(login_url='login')
def create_room(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        form = RoomForm(request.POST)
        topic, created = Topic.objects.get_or_create(name=topic_name)
        ChatRoom.objects.create(
            room_host = request.user,
            room_title = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')

        )
       
        return redirect('home-page')


    return render(request, 'Chat/roomform.html',{"topics":topics ,"form":form})


@login_required(login_url='login')
def update_room(request, pk):
    topics = Topic.objects.all()
    room = ChatRoom.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.room_host:
        return HttpResponse("Not Allowed to Update ")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name'),
        room.room_title = topic
        room.description = request.POST.get('description')
        room.save() 
        return redirect('home-page')
    return render(request, 'Chat/roomform.html',{"form":form,"topics":topics})

def delete_room(request, pk):
    room = ChatRoom.objects.get(id=pk)
    if request.user != room.room_host:
        return HttpResponse("Not Allowed to Delete ")

    if request.method == 'POST':
            room.delete()
            return redirect('home-page')
    return render(request, 'Chat/delete.html',{"room":room})

def delete_message(request, pk):
    message_del = Message.objects.get(id=pk)
    if request.user != message_del.user:
        return HttpResponse("Not Allowed to Update ")

    if request.method == 'POST':
            message_del.delete()
            return redirect('home-page')
    return render(request, 'Chat/delete.html',{"message_del":message_del})

@login_required(login_url='login')
def profile(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        d_form = UpdateDetails(request.POST, instance=request.user)
        p_form = UpdateProfile(request.POST,request.FILES, instance=request.user.profile)
        if d_form.is_valid() and p_form.is_valid():
            d_form.save()
            p_form.save() 
            messages.info(request, 'Account Information Update succesful')
            return redirect('profile')
    else:
        d_form = UpdateDetails(instance=request.user)
        p_form = UpdateProfile(instance= request.user.profile)
    
    context = {"d_form":d_form,"p_form":p_form, "topics":topics}

    return render(request, 'Chat/profile.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'Account creation for {username} succesful')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html',{"form":form})