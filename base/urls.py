
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.lobby),
    path('room/', views.room),
    path('get_token/',views.getToken),
    path('create_member/',views.createMember),
    path('get_member/',views.getMember),
    path('leave_member/',views.leaveMember)
]
