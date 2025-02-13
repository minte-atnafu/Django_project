from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.

rooms = [
    {'id':1, 'name':'the fastest man'},
    {'id':2, 'name':'the tallest man'},
    {'id':3, 'name':'the strongest man'}
]

def home(request):
     rooms=Room.objects.all()
     context={'rooms': rooms}
     return render(request, 'base/home.html', context)

def room(request, pk):
    room= Room.objects.get(id=pk)
    context={'room':room}
    return render(request, 'base/room.html',context)