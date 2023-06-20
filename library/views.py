from django.shortcuts import redirect
from . import settings
# Create your views here.

def goHome(request):
    return redirect(settings.LOGIN_REDIRECT_URL)