from django import forms
from .models import Room,RoomMember
from django.core.exceptions import ObjectDoesNotExist

class RoomForm(forms.ModelForm):
    
    class Meta:
        model = Room
        fields = ("name",)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter room name...'}),
        }


    # def validate(self,data):
    #     print('validationError')        
    #     if(Room.objects.filter(name=data['name'],active=True).exists()):
    #             return self.data
    #     else:
    #         print('validationError')
    #         raise forms.ValidationError('Room Name is not Unique!!!' )
    

class RoomMemberForm(forms.ModelForm):

    class Meta:
        model = RoomMember
        fields = ("name","room_name")
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name...'}),
            'room_name': forms.TextInput(attrs={'placeholder': 'Enter room name...'}),
        }
        error_messages={
            'room_name': {
                'DoesNotExist': ("Room Doesn't exists, Please create one!!"),
            }
        }

    def clean(self):
        data=self.cleaned_data
        if('room_name' in data):
            room=Room.objects.get(name=data['room_name'])
            if(room.active==True):
                return self.cleaned_data
            else:
                raise forms.ValidationError('This room has ended!!!' )
        else:
            raise forms.ValidationError("Room Doesn't exists, Please create one!!")

        


        