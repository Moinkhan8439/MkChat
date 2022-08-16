
import os,time,random
from .models import RoomMember
from utilities.RtcTokenBuilder import RtcTokenBuilder

def generateUID(room):
    uid=random.randint(1,230)
    if(RoomMember.objects.filter(room_name=room , uid=uid).exists()):
        generateUID(room)
    else:
        return uid


def generateRTCToken(room,uid,role):
    appId=os.environ.get('Agora_app_id')
    appCertificate= os.environ.get('Agora_app_certificate')
    channelName=room
    uid=uid
    role=role
    expiryInTimeSecond = 3600*24
    currentTimeStamp=time.time()
    print(currentTimeStamp)
    expiry=currentTimeStamp + expiryInTimeSecond
    token=RtcTokenBuilder.buildTokenWithUid(appId,appCertificate,channelName,uid,role,expiry)
    return token