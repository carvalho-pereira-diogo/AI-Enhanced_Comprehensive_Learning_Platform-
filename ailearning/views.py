from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from bachelorproject import settings

# Create your views here.
def home(request):
    return render(request, 'ailearning/index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists, Try other username!")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists, Try other email!")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "Your account has been created successfully")
        
        # Welcome email
        subject = 'Welcome to Smartmentor'
        message = f'Hi {myuser.first_name}, thank you for registering in Smartmentor. We are glad to have you with us.'
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        return redirect('signin')
    
    return render(request, 'ailearning/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'ailearning/index.html', {'fname': fname})
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home")
        
    return render(request, 'ailearning/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('home')

def dashboard(request):
    return render(request, 'ailearning/dashboard.html')