from email import message
from multiprocessing import context
from urllib.request import Request
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import ChatRoom, Topic, Message
from .forms import RoomForm, UpdateDetails, UpdateProfile


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
    context = {"rooms":rooms, "topics":topics, "comments":comments}
    return render(request, 'Chat/index.html', context)

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

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            room = form.save(commit =False)
            room.room_host = request.user 
            room.save()
            return redirect('home-page')


    return render(request, 'Chat/roomform.html',{"form":form})


@login_required(login_url='login')
def update_room(request, pk):
    room = ChatRoom.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.room_host:
        return HttpResponse("Not Allowed to Update ")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('home-page')
    return render(request, 'Chat/roomform.html',{"form":form})

def delete_room(request, pk):
    room = ChatRoom.objects.get(id=pk)
    if request.method == 'POST':
            room.delete()
            return redirect('home-page')
    return render(request, 'Chat/delete.html',{"room":room})



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