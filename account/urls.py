from django.urls import path, re_path
from . import views
app_name = 'account'

urlpatterns = [
    path('sign-up/', views.register, name = 'register'),
    path('login/', views.loginUser, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('profile/', views.profileUser, name = 'profile'),
    path('profile/delete-photo/', views.delete_photo, name='delete_photo'),
    
    # 404
    path('<str:text>/', views.notFound3),
    path('sign-up/<str:text>/', views.notFound3),
    path('login/<str:text>/', views.notFound3),
    path('logout/<str:text>/', views.notFound3),
    path('profile/<str:text>/', views.notFound3),
    path('edit-profile/<str:text>/', views.notFound3),
]