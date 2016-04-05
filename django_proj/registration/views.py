from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User

from registration.forms import RegistrationForm, LoginForm
from registration.models import Account
from registration.utils import email_to_username

def login_page(request, _next="/home/"):
    if not request.user.is_anonymous():
        return redirect('/home/')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(_next)
    else:
        form = LoginForm()
        
    return render(
                  request,
                  'registration/login.html',
                  {'form': form, 'next': _next, 'title': "Please Login"}
                  )

@csrf_protect
def register(request):
    
    if not request.user.is_anonymous():
        return redirect('/home/')
    
    if request.method == 'POST':
        title = "Update Profile"
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create(username=email_to_username(email),
                                       email=email)
            user.set_password(password)
            user.save()
            account = Account.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                middle_name=form.cleaned_data['middle_name'],
                last_name=form.cleaned_data['last_name'],
                mobile_no=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email']
            )
            return redirect('/register/success/')
    else:
        title = "Create New Profile"
        form = RegistrationForm()
   
    return render(
                  request,
                  'registration/register.html',
                  {'form': form, 'title': title}
                  )

@login_required
def edit(request):
    curr_user = request.user
    if request.method == 'POST':
        form = RegistrationForm(request.POST, user=curr_user)
        
        if form.is_valid():
            curr_user.account.first_name = form.cleaned_data['first_name']
            curr_user.account.middle_name = form.cleaned_data['middle_name']
            curr_user.account.last_name = form.cleaned_data['last_name']
            curr_user.account.mobile_no = form.cleaned_data['phone_number']
            curr_user.account.email = form.cleaned_data['email']
            curr_user.account.save()
            
            return redirect('/register/success/')
    else:
        form = RegistrationForm(user=curr_user)
   
    return render(
                  request,
                  'registration/register.html',
                  {'form': form, 'title': 'Update Profile'}
                  )
    
def register_success(request):
    return render(
                  request, 
                  'registration/succ.html',
                  )
 
def logout_page(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    curr_user = request.user
    return render(
                  request,
                  'registration/home.html',
                  {'user': curr_user }
                  )
