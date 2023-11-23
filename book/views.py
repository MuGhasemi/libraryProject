from datetime import date ,datetime
import sweetify
import os
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Book, Genre, Author, BookInstance
from .forms import InsertBookForm, EditBookForm, SearchBoxForm, AddBookInstanceForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.


def about(request):
    return render(request, 'book/about.html')

# --- All function for Book model ---

def home(request):
    search = SearchBoxForm(request.GET)
    if search.is_valid():
        cd = search.cleaned_data['search']
        books = Book.objects.filter(name__icontains=cd, status='a').order_by('id')
        if not books.exists():
            books = Book.objects.filter(status = 'a').order_by('id')
            sweetify.error(request, 'کتاب وجود ندارد')
    else:
        books = Book.objects.filter(status = 'a')
    for book in books:
        genres = book.genre.all()
        book.genres = genres
    genres = Genre.objects.all()
    authors = Author.objects.all()
    context = {
        'books': books,
        'genres':genres,
        'authors':authors,
        'search': search,
    }
    return render(request, 'book/home.html', context)

def detail(request, pk):
    bookDetail = Book.objects.get(id=pk)
    if request.method == 'POST':
        instance = AddBookInstanceForm(request.POST)
        if instance.is_valid():
            if request.user.is_authenticated:
                cd = instance.cleaned_data
                borrower = request.user
                if bookDetail.status == 'a' and cd['due_back'] > date.today():
                    BookInstance.objects.create(book=bookDetail,
                                                due_back=cd['due_back'],
                                                borrower=borrower,
                                                status= 'o')
                    bookDetail.status = 'o'
                    bookDetail.save()
                    sweetify.success(request, 'نمونه با موفقیت اضافه شد')
                    return redirect('/book/all-instances/')
                else:
                    if cd['due_back'] <= date.today():
                        sweetify.error(request, 'تاریخ شما باید یک روز بیشتر از تاریخ فعلی باشد')
                    elif bookDetail.status != 'a':
                        sweetify.error(request, 'کتاب موجود نیست')
            else:
                return redirect(settings.LOGIN_URL + '?next=' + request.path)
        else:
            sweetify.error(request, 'عملیات ناموفق بود')
            return redirect(f'/book/detail/{pk}')
    else:
        instance = AddBookInstanceForm()
    context = {'bookDetail': bookDetail,
               'form': instance,}
    return render(request, 'book/detail.html', context)

@login_required
def addBook(request):
    if not request.user.is_staff:
        return redirect('book:home')
    if request.method == 'POST':
        book = InsertBookForm(request.POST, request.FILES)
        if book.is_valid():
            book.save()
            sweetify.success(request, 'کتاب با موفقیت اضافه شد')
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            sweetify.error(request, 'افزودن کتاب ناموفق بود')
            return redirect('/book/insert-book/')
    else:
        book = InsertBookForm()
        context = {
            'form': book
        }
    return render(request, 'book/insertBook.html', context)

@login_required
def editBook(request, pk):
    if not request.user.is_staff:
        return redirect('book:home')
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        old_photo_name = None
        if book.bookImage.name:
            old_photo_path = book.bookImage.path
            old_photo_name = book.bookImage.name
        edit_book = EditBookForm(request.POST,request.FILES ,instance = book)
        if edit_book.is_valid():
            new_book_image = request.FILES.get('add-book-img')
            if new_book_image and new_book_image.name != old_photo_name:
                book.bookImage = new_book_image
                if old_photo_name:
                    os.remove(old_photo_path)
            else:
                edit_book.cleaned_data['bookImage'] = None
            edit_book.save()
            sweetify.success(request, 'ویرایش کتاب با موفقیت انجام شد')
            return redirect(f'/book/detail/{pk}')
        else:
            sweetify.error(request, 'ویرایش کتاب ناموفق بود')
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
    if book.bookImage:
        bookImage = book.bookImage.path
        os.remove(bookImage)
    book.delete()
    sweetify.success(request, 'کتاب با موفقیت حذف شد')
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
    if bookInstances :
        for instance in bookInstances:
            if instance.due_back <= today and time <= datetime.now().hour:
                instance.delete()
                book = Book.objects.get(id=instance.book.id)
                sweetify.warning(request,  f'{ instance.book }, به دلیل پایان مهلت زمانی حذف شد', button='Ok', timer=3000)
                book.status = 'a'
                book.save()
                return redirect('/book/all-instances/')
    else:
        sweetify.warning(request, 'کتابی ثبت نشده است', button='Ok', timer=3000)
    context = {'bookInstances': bookInstances
                }
    return render(request, 'book/showBookInstance.html', context)

def notFound2(request, text):
    return render(request, 'partials/404.html', {'exception': text})