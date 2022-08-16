
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.lobby),
    path('get_key/',views.getKey),
    path('room/', views.room),
    path('join-room/', views.joinRoom,name='join-room'),
    path('get_token/',views.getToken),
    path('create_member/',views.createMember),
    path('get_member/',views.getMember),
    path('leave_member/',views.leaveMember),
    path('create-room/',views.createRoom,name='create-room')
]
