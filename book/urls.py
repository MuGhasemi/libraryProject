from django.urls import path, re_path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('insert-book/', views.addBook, name = 'addBook'),

    path('detail/<int:pk>/', views.detail, name = 'detail'),
    path('detail/<int:pk>/edit', views.editBook, name = 'editBook'),
    path('detail/<int:pk>/delete', views.deleteBook, name = 'deleteBook'),

    path('all-genres/', views.showGenres, name = 'allGenres'),

    path('all-authors/', views.showAuthors, name = 'allAuthors'),

    path('all-instances/', views.showBookInstance, name = 'allInstances'),
    path('add-instance/<int:pk>', views.addBookInstance, name = 'addinstance'),

    path('about/', views.about, name = 'about'),
]