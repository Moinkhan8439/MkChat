from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .forms import UserLoginForm,UserCreationForm


def user_login(request):
    form=UserLoginForm(data=request.POST or None)
    if(form.is_valid()):  
        data=form.cleaned_data
        print('valid-form')     
        user=auth.authenticate(username=data['username'],password=data['password'])
        auth.login(request,user)
        messages.info(request,'Successfully logged in!')
        return redirect('/create-room/')
    else:
        print('get-form')
        if 'next' in request.GET:
            messages.add_message(request, messages.INFO, 'Login is required to create a Room.')
        return render(request,'./base/lobby.html',{'Form':form,'cusUrl':'/accounts/login/',"button":'Login'})


def user_logout(request):
    auth.logout(request)
    messages.info(request, messages.INFO, 'Logged out Successfully.')
    return redirect('/')



# @login_required(login_url='/user-login')
# def profile_creation(request):
#     if request.method == "POST":
#         city=request.POST['city']
#         number=request.POST['contact_number']
#         s=student.objects.filter(user=request.user).update(city=city,contact_number=number)
#         messages.info(request,'profile Created!!')
#         return redirect('home')
#     else:
#         s=student.objects.filter(user=request.user).values()
#         city=s[0]['city']
#         number=s[0]['contact_number']
#         context={"user" : request.user , "city": city , "number" : number}
#         return render(request,'profile.html', context)



def user_register(request):
    form=UserCreationForm(request.POST or None)
    if(form.is_valid()):
        data=form.cleaned_data
        form.save()
        user=auth.authenticate(username=data['username'],password=data['password'])
        auth.login(request,user)
        messages.info(request,'User Registered and logged in!')
        return redirect('/')
    else:
        return render(request,'./base/lobby.html',{'Form':form,'cusUrl':'/accounts/register/',"button":'SignUp'})




# def user_register(request):
#     if(request.method == 'POST'):
#         username=request.POST['username']
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         email=request.POST['email']
#         password1=request.POST['password1']
#         password2=request.POST['password2']
#         if( password1 == password2 and password1!=''):
#             if(User.objects.filter(username=username).exists()):
#                 messages.info(request,'Username taken!!')
#                 return redirect('user-register')
#             elif(User.objects.filter(email=email).exists()):
#                 messages.info(request,'email taken!!')
#                 return redirect('user-register')
#             else:
#                 user=User.objects.create_user(username=username , first_name=first_name ,last_name =last_name , email=email,password =password1)
#                 user.save()
#                 messages.info(request,'User Registered')
#                 return render(request,'login.html')
#         else:
#             messages.info(request,'Password doesnt match!!')
#             return redirect('user-register')
#     else:
#         return render(request,'register.html')