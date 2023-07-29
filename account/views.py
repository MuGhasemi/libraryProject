import os
from django.shortcuts import render, redirect
from .forms import EditProfileFrom, EditUserForm, RegisterUserForm, LoginUserForm
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
            if cd['password'] == cd['confirm_password']:
                user = User.objects.create_user(username = cd['username'],
                                                first_name = cd['first_name'],
                                                last_name = cd['last_name'],
                                                email = cd['email'],
                                                password = cd['password'])
                user.save()
                Profile.objects.create(user=user)
                messages.success(request, 'create account successfully', 'success')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect(settings.LOGIN_URL)
            else:
                messages.success(request, 'password not match!', 'danger')
                return redirect(settings.SIGN_UP_URL)
        else:
            messages.success(request, 'create account failed', 'danger')
            return redirect(settings.SIGN_UP_URL)
    else:
        registerForm = RegisterUserForm()
    context = {'registerform': registerForm}
    return render(request, 'account/registerUser.html', context)

def loginUser(request):
    if request.method == 'POST':
        dataForm = LoginUserForm(request.POST)
        if dataForm.is_valid():
            cd = dataForm.cleaned_data
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
        loginForm = LoginUserForm()
    context = {'loginform': loginForm}
    return render(request, 'account/loginUser.html', context)

@login_required
def logoutUser(request):
    messages.success(request, f'{ request.user }, thank your for visiting us site', 'success')
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)

@login_required
def profileUser(request):
    if request.method == 'POST':
        old_photo_name = None
        profileImage = request.user.profile.profileImage
        if profileImage.name:
            old_photo_path = profileImage.path
            old_photo_name = profileImage.name
        editUser = EditUserForm(request.POST, instance = request.user)
        editProfile = EditProfileFrom(request.POST, request.FILES, instance = request.user.profile)
        if editUser.is_valid() and editProfile.is_valid():
            new_profile_image = editProfile.cleaned_data.get('profileImage')
            if new_profile_image and new_profile_image.name != old_photo_name:
                if old_photo_name:  # only delete old photo if it exists
                    os.remove(old_photo_path)
            else:
                editProfile.cleaned_data['profileImage'] = None
            editUser.save()
            editProfile.save()
            messages.success(request, 'Edit successfully', 'success')
        else:
            messages.success(request, 'Edit failed', 'warning')
        return redirect('/account/profile/')
    else:
        editUser = EditUserForm(instance = request.user)
        editProfile = EditProfileFrom(instance = request.user.profile)
        context = {
            'editUser': editUser,
            'editProfile': editProfile,
            'profileImage':request.user.profile.profileImage,
            }
        return render(request, 'account/profileUser.html', context)

def delete_photo(request):
    profile = request.user.profile
    if request.method == 'GET':
        if profile.profileImage:
            profile.profileImage.delete()
            profile.profileImage = None
            profile.save()
            messages.success(request, 'image profile deleted', 'success')
            return redirect('/account/profile/')
        else:
            messages.success(request, "don't have image profile", 'warning')
            return redirect('/account/profile/')
    else:
        messages.success(request, 'image profile failed', 'warning')
        return redirect('/account/profile/')


def notFound3(request, text):
    return render(request, 'partials/404.html', {'exception': text})