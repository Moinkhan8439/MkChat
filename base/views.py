from django.shortcuts import render
from django.http import JsonResponse
from utilities.RtcTokenBuilder import RtcTokenBuilder
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
import random
import time
import json

# Create your views here.

def getToken(request):
    appId='50b57bc7553f46b5a1320571ff21c002'
    appCertificate='46d85ca89c4b4184967139f4dd80c6fa'
    channelName=request.GET.get('channel')
    uid=random.randint(1,230)
    role=1
    expiryInTimeSecond=3600*24
    currentTimeStamp=time.time()
    expiry=currentTimeStamp + expiryInTimeSecond
    token=RtcTokenBuilder.buildTokenWithUid(appId,appCertificate,channelName,uid,role,expiry)
    return JsonResponse({'token':token,'uid':uid},safe=False)

@csrf_exempt
def createMember(request):
    data=json.loads(request.body)
    member,created=RoomMember.objects.get_or_create(
        name=data['username'],
        uid=data['UID'],
        room_name=data['room'],
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
    member.save()
    message=f'{member.name} left !!!'
    return JsonResponse({'message': message},safe=False) 

def lobby(request):
    return render(request,'base/lobby.html')


def room(request):
    return render(request,'base/room.html')