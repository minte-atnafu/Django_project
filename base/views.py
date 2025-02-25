from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Topic,User, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

rooms = [
    {'id':1, 'name':'the fastest man'},
    {'id':2, 'name':'the tallest man'},
    {'id':3, 'name':'the strongest man'}
]

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
 

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
           user=User.objects.get(username=username)  
        except:
           messages.error(request,'user does not exsit')    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
           messages.error(request, 'username or password does not exist')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an error occuredduring registration')
    return render(request, 'base/login_register.html',{'form':form})

def home(request):
    p = request.GET.get('p', '').strip()  # Get 'p' from URL
    rooms = Room.objects.filter(Q(topic__name__icontains=p) |
                                Q(name__icontains=p) |
                                Q(description__icontains=p)) if p else Room.objects.all()
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)
   

def room(request, pk):
    room= Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body = request.POST.get('body')
        )
        return redirect('room', pk=room.id)
    context={'room':room, 'room_messages':room_messages}
    return render(request, 'base/room.html',context)
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse('You must be logged in to edit a room.')

    # Check if the user is the host
    if request.user != room.host:
        return HttpResponse('You do not have permission here.')

    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('you do not have permission here') 
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


