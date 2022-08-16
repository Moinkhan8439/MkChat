from datetime import datetime
from operator import le
from django.conf import settings
from django.db import models

# Create your models here.

class Room(models.Model):
    name=models.CharField(unique=True,max_length=50)
    created_on=models.DateTimeField(auto_now=False, auto_now_add=False)
    ended_on = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    host=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True)
    active=models.BooleanField()

    def __str__(self):
        return self.name
    

class RoomMember(models.Model):
    name=models.CharField(max_length=200)
    uid=models.CharField( max_length=200)
    #room_name=models.CharField(max_length=50)
    room_name=models.ForeignKey(Room,to_field='name',on_delete=models.CASCADE)
    active=models.BooleanField()
    RTCToken=models.CharField( max_length=250)
    join_time=models.DateTimeField( auto_now=False, auto_now_add=True)
    leave_time=models.DateTimeField( auto_now=False, auto_now_add=False, null=True)

    def __str__(self):
        return self.name
