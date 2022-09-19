
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from utilities.RtcTokenBuilder import RtcTokenBuilder

from .models import RoomMember,Room
from .forms import RoomForm,RoomMemberForm
from .utils import generateUID,generateRTCToken

import time
import json
import os


ROLE_HOST=1
ROLE_ATTENDEE=2
appId=settings.APP_ID
appCertificate=settings.APP_CERTIFICATE

# Create your views here.

def getToken(request):  
    channelName=request.GET.get('channel')
    uid=generateUID(channelName)
    role=1
    expiryInTimeSecond = 3600*24
    currentTimeStamp=time.time()
    print(currentTimeStamp)
    expiry=currentTimeStamp + expiryInTimeSecond
    token=RtcTokenBuilder.buildTokenWithUid(appId,appCertificate,channelName,uid,role,expiry)
    return JsonResponse({'token':token,'uid':uid},safe=False)

@csrf_exempt
def createMember(request):
    data=json.loads(request.body)
    print(f"room name: {data['room']}")
    room=Room.objects.get(name=data['room'])
    print(room)
    member,created=RoomMember.objects.get_or_create(
        name=data['username'],
        uid=data['UID'],
        room_name=room,
        RTCToken=data['token'],
        active=True
    )
    return JsonResponse({'name':data['username']},safe=False)


def getMember(request):
    uid=request.GET.get('UID')
    room_name=request.GET.get('room')
    member=RoomMember.objects.get(uid=uid,room_name=room_name)
    name= member.name
    return JsonResponse({'name':name} , safe=False)


@csrf_exempt
def leaveMember(request):
    data=json.loads(request.body)    
    member=RoomMember.objects.get(uid=data['UID'],room_name=data['room'],active=True)
    member.active=False
    member.leave_time=timezone.now()
    member.save()
    message=f'{member.name} left !!!'
    memberCount=RoomMember.objects.filter(room_name=data['room'],active=True).count()
    if(memberCount == 0):
        room=Room.objects.get(name=data['room'],active=True)
        room.active=False
        room.ended_on=timezone.now()
        room.save()
    return JsonResponse({'message': message},safe=False) 


@login_required(login_url='/accounts/login/')
def createRoom(request):
    createRoomForm=RoomForm(request.POST or None)
    if createRoomForm.is_valid():
        obj=createRoomForm.save(commit=False)
        obj.created_on=timezone.now()
        obj.host=request.user
        obj.active=True
        obj.save()
        print(request.user)
        joinRoomForm=RoomMemberForm(initial={
            'room_name':obj.name,
            'name': obj.host.username
        })
        print(obj.host.username)
        return render(request,'base/lobby.html',{"Form":joinRoomForm,'cusUrl':'/join-room/',"button":"Join Room"})
    else:
        print(createRoomForm.errors)
        return render(request,'base/lobby.html',{"Form":createRoomForm,"cusUrl":'/create-room/',"button":'Create Room'})




def joinRoom(request):
    joinRoomForm=RoomMemberForm(request.POST or None)
    if request.method == 'POST':
        if joinRoomForm.is_valid():            
            print("valid formm")
            data=joinRoomForm.cleaned_data
            room_name=data['room_name'].name
            member=joinRoomForm.save(commit=False)
            member.uid=generateUID(room_name)
            member.RTCToken=generateRTCToken(room_name,member.uid,ROLE_HOST)
            member.active=True
            member.save()
            request.session['room']=member.room_name.name
            request.session['token']=member.RTCToken
            request.session['username']=member.name
            request.session['UID']=member.uid
            request.session['APP_ID']='50b57bc7553f46b5a1320571ff21c002'
            #request.session['APP_id']=os.environ.get('Agora_app_id')
            request.session.modified=True
            return redirect('/room/')
        else:
            print(joinRoomForm.errors)
            return render(request,'base/lobby.html',{"Form":joinRoomForm,"cusUrl":'/join-room/',"button":'Join Room'})
    else:
        if('username' in request.session and 'room' in request.session):
                joinRoomForm=RoomMemberForm(initial={
                'room_name':request.session['room'],
                'name': request.session['username']
                })
        return render(request,'base/lobby.html',{"Form":joinRoomForm,"cusUrl":'/join-room/',"button":'Join Room'})


def lobby(request):
    return render(request,"base/lobby.html")


def room(request):
    print("inside room")
    return render(request,"base/room.html")


def getKey(request):
    return JsonResponse({'id': appId },safe=False)