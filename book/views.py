from datetime import date ,datetime
import os
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Book, Genre, Author, BookInstance
from .forms import InsertBookForm, EditBookForm, SearchBoxForm, AddBookInstanceForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.


def about(request):
    books = Book.objects.all()
    context = {'books':books}
    return render(request, 'book/about.html', context)

# --- All function for Book model ---

def home(request):
    search = SearchBoxForm(request.GET)
    if search.is_valid():
        cd = search.cleaned_data['search']
        books = Book.objects.filter(name__icontains = cd, status = 'a')
        if not books.exists():
            books = Book.objects.filter(status = 'a')
            messages.error(request, 'Book not exist.', 'danger')
    else:
        books = Book.objects.filter(status = 'a')
    for book in books:
        genres = book.genre.all()
        book.genres = genres
    context = {
        'books': books,
        'search': search,
    }
    return render(request, 'book/home.html', context)

def detail(request, pk):
    bookDetail = Book.objects.get(id=pk)
    context = {'bookDetail': bookDetail}
    return render(request, 'book/detail.html', context)

@login_required
def addBook(request):
    if request.method == 'POST':
        book = InsertBookForm(request.POST, request.FILES)
        if book.is_valid():
            book.save()
            messages.success(request, 'Book add successfully.', 'success')
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.success(request, 'Book add failed.', 'danger')
            return redirect('/book/insert-book')
    else:
        book = InsertBookForm()
        context = {
            'form': book
        }
    return render(request, 'book/insertBook.html', context)

@login_required
def editBook(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        old_photo_name = None
        if book.bookImage.name:
            old_photo_path = book.bookImage.path
            old_photo_name = book.bookImage.name
        edit_book = EditBookForm(request.POST,request.FILES ,instance = book)
        if edit_book.is_valid():
            new_book_image = edit_book.cleaned_data.get('bookImage')
            if new_book_image and new_book_image.name != old_photo_name:
                if old_photo_name:
                    os.remove(old_photo_path)
            else:
                edit_book.cleaned_data['bookImage'] = None
            edit_book.save()
            messages.success(request, 'Book edit successfully.', 'success')
            return redirect(f'/book/detail/{pk}')
        else:
            messages.success(request, 'Book edit failed.', 'danger')
            return redirect(f'/book/detail/{pk}')
    else:
        edit_book = EditBookForm(instance = book)
        context = {
            'editForm': edit_book,
            'pk': pk,
            'bookImage': edit_book.instance.bookImage
            }
        return render(request, 'book/editDetailBook.html', context)

@login_required
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    bookImage = book.bookImage.path
    book.delete()
    os.remove(bookImage)
    messages.success(request, 'Book deleted successfully.', 'success')
    return redirect(settings.LOGIN_REDIRECT_URL)

# --- All function for Genre model---

def showGenres(request):
    genres = Genre.objects.all()
    context = {'genres': genres}
    return render(request, 'book/showGenres.html', context)

# --- All function for Author model ---

def showAuthors(request):
    authors = Author.objects.all()
    context= {'authors': authors}
    return render(request, 'book/showAuthors.html', context)

# --- All function for BookInstance model ---

@login_required
def showBookInstance(request):
    today = date.today()
    time = 23
    bookInstances = BookInstance.objects.filter(borrower = request.user)
    for instance in bookInstances:
        if instance.due_back <= today and time <= datetime.now().hour:
            instance.delete()
            book = Book.objects.get(id=instance.book.id)
            messages.success(request,  f'{instance.book} book was deleted due to timeout.', 'warning')
            book.status = 'a'
            book.save()
    context = {'bookInstances': bookInstances
                }
    return render(request, 'book/showBookInstance.html', context)


@login_required
def addBookInstance(request, pk):
    bookTitle = Book.objects.get(id=pk)
    if request.method == 'POST':
        instance = AddBookInstanceForm(request.POST)
        if instance.is_valid():
            cd = instance.cleaned_data
            borrower = request.user
            BookInstance.objects.create(book=bookTitle,
                                        due_back=cd['due_back'],
                                        borrower=borrower,
                                        status= 'o')
            bookTitle.status = 'o'
            bookTitle.save()
            messages.success(request, 'Instance add successfully.', 'success')
            return redirect('/book/all-instances/')
        else:
            messages.success(request, 'Instance add failed.', 'danger')
            return redirect(f'/book/add-instance/{pk}')
    else:
        instance = AddBookInstanceForm()
    context = {'form': instance,
                'user': request.user,
                'book': bookTitle}
    return render(request, 'book/addBookInstance.html', context)

def notFound2(request,text):
    return HttpResponseNotFound(f'{text} page not found')