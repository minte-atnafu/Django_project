from django.urls import path
from . import views

urlpatterns =[
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('register/', views.registerUser, name='register'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name="room"),
    path('room-form/', views.createRoom, name='room-form'),
    path('update-room/<str:pk>/', views.updateRoom, name= 'update-room' ),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room')

]