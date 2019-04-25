from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import smtplib
from django.contrib.auth import get_user_model
from pollapp.models import MakePoll, Vote

def HomePage(requset):
    '''HomePage of WebApp'''
    return render(requset,'regLogin/HomePage.html',)

def UserRegistration(request):
    if request.method == 'POST':
    # Getting values from HTML form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username already has been taken')
                return redirect('newUserRegister')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is being used')
                    return redirect('newUserRegister')
                else:
                    user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    # messages.success(request, f'You are now registered with username:{username}')
                    return redirect('HomePage')
        else:
            messages.error(request, 'Passwords do not match..')
            return redirect('newUserRegister')
    else:
        return render(request, 'regLogin/registration.html')


def Login(request):
    '''User Login Function'''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, f'You are now logged in as username:{username}')
            return redirect('signedIn')
        else:
            messages.error(request, 'Invalid credentials..')
            return redirect('UserLogin')
    else:
        return render(request,'regLogin/login.html')

def Logout(request):
    '''User Logout Function'''

    auth.logout(request)
    return redirect('HomePage')

def PasswordResetView(request):
    if request.method == 'POST':
        email = request.POST['email']# Getting email from HTML
        user = User.objects.filter(email__exact = email).first() # Fetching email from User Table
        if user:
            message = render_to_string('regLogin/password_reset_email.html', {
                'domain': request.META['HTTP_HOST'],
                'uid': user.pk,
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https'
            })
            connection = smtplib.SMTP('smtp.gmail.com',587)
            connection.ehlo()
            connection.starttls()
            connection.login('write your gmail account','password')
            connection.sendmail('write your gmail account',email,message)
            connection.quit()
            return render(request,'regLogin/password_reset_done.html')
        else:
            messages.error(request, 'Enail does not Exist..')
            return redirect('password_reset')
    else:
        return render(request,'regLogin/password_reset_form.html')


def PasswordResetDoneView(request):
    return render(request,'regLogin/password_reset_done.html')

def PasswordResetConfirmView(request,uidb64 = None, token = None,*args, **kwargs):
    if request.method == 'POST':
        password = request.POST['password1']
        password2 = request.POST['password2']
        UserModel = get_user_model()
        if password == password2:
            UserMode = get_user_model()
            uid = uidb64
            print(uid)
            user = UserModel._default_manager.get(pk=uid)
            user.set_password(password)
            user.save()
            return redirect('password_reset_complete')
        else:
            messages.error(request,'both password don\'t match.')
            return render(request,'regLogin/password_reset_confirm.html',{'uidb64':uidb64, 'token':token})
    else:
        return render(request,'regLogin/password_reset_confirm.html',{'uidb64':uidb64, 'token':token})

def PasswordResetCompleteView(request):
    return render(request,'regLogin/password_reset_complete.html')


def Profile(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_detail = User.objects.get(id = user_id)
        Questions = MakePoll.objects.filter(owner = user_detail)
        if Questions:
            return render(request,'regLogin/profile.html',{'Questions':Questions,'user_detail':user_detail})
        else:
            Questions = None
            return render(request,'regLogin/profile.html',{'Questions':Questions,'user_detail':user_detail})
