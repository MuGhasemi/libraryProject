from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from . import settings
# Create your views here.

def goHome(request):
    return redirect(settings.LOGIN_REDIRECT_URL)

def notFound1(request,text):
    return HttpResponseNotFound(f'{text} page not found')