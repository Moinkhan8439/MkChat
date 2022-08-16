from django.contrib.auth.forms import AuthenticationForm,UsernameField, UserCreationForm
from django import forms
from django.contrib.auth.models import User,auth

class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,'placeholder': 'Enter username...'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",'placeholder': 'Enter password...'}),
    )
    # class Meta:
    #     widgets={
    #         'username': forms.TextInput(attrs={'placeholder': 'Enter username...'}),
    #         'password': forms.TextInput(attrs={'placeholder': 'Enter password...'}),
    #     }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = auth.authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    # def validate(self,data):
    #     print('validationError')        
    #     if(Room.objects.filter(name=data['name'],active=True).exists()):
    #             return self.data
    #     else:
    #         print('validationError')
    #         raise forms.ValidationError('Room Name is not Unique!!!' )
    
class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields=("username","email","password")
        widgets={
            'username': forms.TextInput(attrs={'placeholder': 'Enter username...'}),
            'password': forms.TextInput(attrs={'placeholder': 'Enter password...'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter email...'}),
        }

    def clean(self):
        data=self.cleaned_data
        if('email' in data and 'username' in data and 'password' in data):
            if(User.objects.filter(username=data['username']).exists()):
                raise forms.ValidationError('Username taken!!')               
            elif(User.objects.filter(email=data['email']).exists()):
                raise forms.ValidationError('Email Already Exists!')
            else:
                return data 
        else:
            return data 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user 
               


        