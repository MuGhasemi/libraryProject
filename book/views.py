from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Genre, Author, BookInstance
from .forms import InsertBookForm, EditBookForm, SearchBoxForm, AddBookInstanceForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
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
    context = {
        'books': books,
        'search': search,
    }
    return render(request, 'book/home.html', context)

def detail(requset, pk):
    bookDetail = Book.objects.get(id=pk)
    def display_genre():
        return ', '.join([genre.title for genre in bookDetail.genre.all()])
    context = {'bookDetail': bookDetail,
               'display_genre':display_genre}
    return render(requset, 'book/detail.html', context)

@login_required
def addBook(request):
    if request.method == 'POST':
        book = InsertBookForm(request.POST)
        if book.is_valid():
            book.save()
            messages.success(request, 'Book add successfully.', 'success')
            return redirect('/book')
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
        edit_book = EditBookForm(request.POST, instance = book)
        if edit_book.is_valid():
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
            'pk': pk
            }
        return render(request, 'book/editDetailBook.html', context)

@login_required
def deleteBook(request, pk):
    Book.objects.get(id=pk).delete()
    messages.success(request, 'Book deleted successfully.', 'success')
    return redirect('/book')

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
    bookInstances = BookInstance.objects.filter(borrower=request.user)
    if request.method == 'GET' and 'search' in request.GET:
        search = SearchBoxForm(request.GET)
        if search.is_valid():
            cd = search.cleaned_data['search']
            if cd != '':
                bookInstances = BookInstance.objects.filter(Q(book__name__icontains=cd))
            else:
                messages.error(request, 'No instances found for this search.', 'danger')
                bookInstances = BookInstance.objects.filter(borrower=request.user)
        else:
            bookInstances = BookInstance.objects.filter(borrower=request.user)
    else:
        search = SearchBoxForm()
    context = {
        'bookInstances': bookInstances,
        'search': search
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

def check_due_back():
    today = date.today()
    book_instances = BookInstance.objects.all()
    for instance in book_instances:
        if instance.due_back == today:
            instance.delete()
            book = get_object_or_404(Book, id=instance.book.id)
            book.status = 'a'
            book.save()