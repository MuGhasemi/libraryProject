from django.urls import path, re_path
from . import views
app_name = 'account'

urlpatterns = [
    path('sign-up/', views.register, name = 'register'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('profile/', views.profileUser, name = 'profile'),
]