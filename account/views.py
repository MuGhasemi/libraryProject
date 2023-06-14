from django.shortcuts import render, redirect
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        dataForm = RegisterUserForm(request.POST)
        if dataForm.is_valid():
            cd = dataForm.cleaned_data
            user = User.objects.create_user(username = cd['username'],
                                            first_name = cd['first_name'],
                                            last_name = cd['last_name'],
                                            email = cd['email'],
                                            password = cd['password'])
            user.save()
            messages.success(request, 'create account successfully', 'success')
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect(settings.LOGIN_URL)
        else:
            messages.success(request, 'create account failed', 'danger')
            return redirect(settings.SIGN_UP_URL)
    else:
        registerform = RegisterUserForm()
    context = {'registerform': registerform}
    return render(request, 'account/registerUser.html', context)

def loginUser(request):
    if request.method == 'POST':
        dataform = LoginUserForm(request.POST)
        if dataform.is_valid():
            cd = dataform.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'login successfully', 'success')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.success(request, 'username or password incorrect', 'danger')
                return redirect(settings.LOGIN_URL)
        else:
            messages.success(request, 'login failed', 'danger')
            return redirect(settings.LOGIN_URL)    
    else:
        loginform = LoginUserForm()
    context = {'loginform': loginform}
    return render(request, 'account/loginUser.html', context)
@login_required
def logoutUser(request):
    messages.success(request, f'{ request.user }, thank your for visiting us site', 'success')
    logout(request)
    return redirect(settings.LOGOUT_URL)

@login_required
def profileUser(request):
    user = request.user
    x = Profile.objects.get(user = user)
    profile = x
    context = {'profile':profile}
    return render(request, 'account/profileUser.html', context)
