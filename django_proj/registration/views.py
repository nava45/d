from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from registration.forms import RegistrationForm
from registration.models import Account
from django.contrib.auth.models import User
from django.contrib.auth.views import login


def login_page(request):
    if request.user.is_anonymous():
        return login(request)
    else:
        return redirect('/home/')

@csrf_protect
def register(request):
    
    if not request.user.is_anonymous():
        return redirect('/home/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password1']
            user = User.objects.create(username=user_name)
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
        form = RegistrationForm()
   
    return render(
                  request,
                  'registration/register.html',
                  {'form': form, 'title': "New Registration"}
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
