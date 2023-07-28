from django.shortcuts import render, redirect
from . import settings
# Create your views here.

def goHome(request):
    return redirect(settings.LOGIN_REDIRECT_URL)

def notFound1(request, text):
    return render(request, 'partials/404.html', {'exception': text})