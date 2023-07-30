import os
import sweetify
from django.shortcuts import render, redirect
from .forms import EditProfileFrom, EditUserForm, RegisterUserForm, LoginUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
                sweetify.success(request, 'create account successfully')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect(settings.LOGIN_URL)
            else:
                sweetify.error(request, 'password not match!')
                return redirect(settings.SIGN_UP_URL)
        else:
            sweetify.error(request, 'create account failed')
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
                sweetify.success(request, 'login successfully')
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                sweetify.error(request, 'username or password incorrect')
                return redirect(settings.LOGIN_URL)
        else:
            sweetify.error(request, 'login failed')
            return redirect(settings.LOGIN_URL)    
    else:
        loginForm = LoginUserForm()
    context = {'loginform': loginForm}
    return render(request, 'account/loginUser.html', context)

@login_required
def logoutUser(request):
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
            sweetify.success(request, 'Edit successfully')
        else:
            sweetify.error(request, 'Edit failed')
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
            sweetify.success(request, 'image profile deleted')
            return redirect('/account/profile/')
        else:
            sweetify.error(request, "don't have image profile")
            return redirect('/account/profile/')
    else:
        sweetify.error(request, 'image profile failed')
        return redirect('/account/profile/')
    

def notFound3(request, text):
    return render(request, 'partials/404.html', {'exception': text})