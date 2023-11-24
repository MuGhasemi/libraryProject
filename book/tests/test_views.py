from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from jalali_date import date2jalali
from datetime import date, timedelta
from model_bakery import baker
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Author, Genre, Book, BookInstance
from ..forms import (SearchBoxForm,
                     AddBookInstanceForm,
                     InsertBookForm,
                     EditBookForm,
                     )


class TestAboutView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_about_view(self):
        response = self.client.get(reverse('book:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/about.html')


class TestHomeView(TestCase):

    def setUp(self):
        self.client = Client()
        self.author = baker.make(Author)
        self.genre = baker.make(Genre)
        self.book1 = Book.objects.create(name='Book 1', author=self.author)
        self.book2 = Book.objects.create(name='Book 2', author=self.author)

    def test_home_view(self):
        response = self.client.get(reverse('book:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/home.html')
        self.failUnless(response.context['search'], SearchBoxForm)
        self.assertEqual(len(response.context['books']), 2)
        self.assertContains(response, 'Book 1')
        self.assertContains(response, 'Book 2')


    def test_home_view_with_valid_search(self):
        response = self.client.get(reverse('book:home'), {'search': 'Book 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 1)
        self.assertContains(response, 'Book 1')
        self.assertNotContains(response, 'Book 2')
        self.assertIn('search', response.context)

    def test_home_view_with_invalid_search(self):
        response = self.client.get(reverse('book:home'), {'search': 'Book 3'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 2)
        self.assertContains(response, 'Book 1')
        self.assertContains(response, 'Book 2')


class TestDetailView(TestCase):

    def setUp(self):
        self.author = baker.make(Author)
        self.genre = baker.make(Genre)
        self.client = Client()
        self.user = User.objects.create_user(username='mmd', password='1234')
        self.book1 = Book.objects.create(name='Book 1', author=self.author)
        self.book2 = Book.objects.create(name='Book 2', author=self.author)
        self.book3 = Book.objects.create(name='Book 3', status='o', author=self.author)
        self.form_data = {'due_back': date2jalali(date.today() + timedelta(weeks=2))}

    def test_detail_view_GET(self):
        response = self.client.get(reverse('book:detail', args=[self.book1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/detail.html')
        self.failUnless(response.context['form'], AddBookInstanceForm)
        self.assertEqual(response.context['bookDetail'], self.book1)
        self.assertContains(response, self.book1.name)
        self.assertNotContains(response, self.book2.name)

    def test_detail_view_POST_without_authentication(self):
        response = self.client.post(reverse('book:detail', args=[self.book1.pk]), data=self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookInstance.objects.count(), 0)
        self.assertRedirects(response, f'/account/login/?next=/book/detail/{self.book1.pk}/')

    def test_detail_view_POST_with_invalid_data(self):
        invalid_form_data = {'due_back': date2jalali(date.today())}
        self.client.login(username='mmd', password='1234')
        # due_back less than today
        response = self.client.post(reverse('book:detail', args=[self.book1.pk]), data=invalid_form_data)
        self.assertEqual(BookInstance.objects.count(), 0)
        self.assertFalse(BookInstance.objects.filter(book=self.book1).exists())
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status, 'a')
        self.assertEqual(response.status_code, 200)

        # bookDetail status equal 'o'
        response = self.client.post(reverse('book:detail', args=[self.book3.pk]), data=self.form_data)
        self.assertEqual(BookInstance.objects.count(), 0)
        self.assertFalse(BookInstance.objects.filter(book=self.book3).exists())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_POST_with_valid_data(self):
        self.client.login(username='mmd', password='1234')
        response = self.client.post(reverse('book:detail', args=[self.book1.pk]), data=self.form_data)
        self.assertTrue(BookInstance.objects.filter(book=self.book1).exists())
        book_instance = BookInstance.objects.get(book=self.book1)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.status, 'o')
        self.assertEqual(BookInstance.objects.count(), 1)
        self.assertEqual(book_instance.borrower, self.user)
        self.assertEqual(book_instance.book, self.book1)
        self.assertEqual(book_instance.status, 'o')
        self.assertEqual(book_instance.due_back, self.form_data['due_back'])
        self.assertRedirects(response, reverse('book:allInstances'))


class TestAddBookView(TestCase):

    def setUp(self):
        self.author = baker.make(Author)
        self.genre = baker.make(Genre)
        self.client = Client()
        self.user = User.objects.create_user(username='mmd', password='1234')
        self.root_user = User.objects.create_superuser(username='root', password='1234')
        self.form_data = {
                        'name': 'new book',
                        'summry': 'summry new book',
                        'genre': [self.genre.id],
                        'author': self.author.id,
                        }

    def test_addBook_view_GET_with_AnonymousUser(self):
        response = self.client.get(reverse('book:addBook'))
        response.user = AnonymousUser()
        self.assertFalse(response.user.is_staff)
        self.assertRedirects(response, '/account/login/?next=/book/insert-book/')
        self.assertEqual(response.status_code, 302)

    def test_addBook_view_GET_without_staff_user(self):
        self.client.login(username='mmd', password='1234')
        response = self.client.get(reverse('book:addBook'))
        response.user = self.user
        self.assertFalse(response.user.is_staff)
        self.assertRedirects(response, reverse('book:home'))
        self.assertEqual(response.status_code, 302)

    def test_addBook_view_GET_with_staff_user(self):
        self.client.login(username='root', password='1234')
        response = self.client.get(reverse('book:addBook'))
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertTemplateUsed(response, 'book/insertBook.html')
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'], InsertBookForm)

    def test_addBook_view_POST_invalid_data(self):
        _invalid_form_data = {
                    'summry': 'summry new book',
                    'genre': [self.genre.id],
                    'author': self.author.id,
                    }
        self.client.login(username='root', password='1234')
        response = self.client.post(reverse('book:addBook'), data=_invalid_form_data)
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(Book.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:addBook'))

    def test_addBook_view_POST_valid_data(self):
        self.client.login(username='root', password='1234')
        response = self.client.post(reverse('book:addBook'), data=self.form_data)
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:home'))
        book = Book.objects.get(name=self.form_data['name'])
        self.assertEqual(book.name, self.form_data['name'])
        self.assertEqual(book.status, 'a')


class TestEditBookView(TestCase):

    def setUp(self):
        self.author = baker.make(Author)
        self.genre = baker.make(Genre)
        self.client = Client()
        self.book1 = Book.objects.create(name='Book 1', author=self.author)
        self.book2 = Book.objects.create(name='Book 2', author=self.author)
        self.book1.genre.add(self.genre)
        self.user = User.objects.create_user(username='mmd', password='1234')
        self.root_user = User.objects.create_superuser(username='root', password='1234')
        self.form_data = {
                        'name': 'new book updated',
                        'summry': 'summry new book updated',
                        'author': self.author.id,
                        'genre': [self.genre.id],
                        }

    def test_editBook_view_GET_with_AnonymousUser(self):
        response = self.client.get(reverse('book:editBook', args=[self.book1.id]))
        response.user = AnonymousUser()
        self.assertFalse(response.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/account/login/?next=/book/detail/{self.book1.id}/edit/')

    def test_editBook_view_GET_without_staff_user(self):
        self.client.login(username='mmd', password='1234')
        response = self.client.get(reverse('book:editBook', args=[self.book1.id]))
        response.user = self.user
        self.assertFalse(response.user.is_staff)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:home'))

    def test_editBook_view_GET_with_staff_user_and_invalid_id(self):
        self.client.login(username='root', password='1234')
        response = self.client.get(reverse('book:editBook', args=[10]))
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(response.status_code, 404)

    def test_editBook_view_GET_with_staff_user_and_valid_id(self):
        self.client.login(username='root', password='1234')
        response = self.client.get(reverse('book:editBook', args=[self.book1.id]))
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/editDetailBook.html')
        self.failUnless(response.context['editForm'], EditBookForm)
        self.assertContains(response, self.book1.name)
        self.assertNotContains(response, self.book2.name)

    def test_editBook_view_POST_without_staff_user(self):
        self.client.login(username='mmd', password='1234')
        response = self.client.post(reverse('book:editBook', args=[self.book1.id]), data=self.form_data)
        response.user = self.user
        self.assertFalse(response.user.is_staff)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:home'))

    def test_editBook_view_POST_with_staff_user_and_invalid_id(self):
        self.client.login(username='root', password='1234')
        response = self.client.post(reverse('book:editBook', args=[10]), data=self.form_data)
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(response.status_code, 404)

    def test_editBook_view_POST_with_staff_user_and_invalid_data(self):
        invalid_form_data = {
                            'name':'',
                            'summry': 'update summary',
                            'author': self.author.id,
                            'genre': [self.genre.id],
                            }
        self.client.login(username='root', password='1234')
        response = self.client.post(reverse('book:editBook', args=[self.book1.id]), data=invalid_form_data)
        response.user = self.root_user
        edit_book = Book.objects.get(id=self.book1.id)
        self.assertTrue(response.user.is_staff)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(edit_book.name, invalid_form_data['name'])
        self.assertNotEqual(edit_book.name, invalid_form_data['summry'])

    def test_editBook_view_POST_with_staff_user_and_valid_data(self):
        self.client.login(username='root', password='1234')
        response = self.client.post(reverse('book:editBook', args=[self.book1.id]), data=self.form_data,)
        response.user = self.root_user
        edit_book = get_object_or_404(Book, id=self.book1.id)
        self.assertTrue(response.user.is_staff)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(edit_book.name, self.form_data['name'])
        self.assertEqual(edit_book.summry, self.form_data['summry'])
        self.assertNotEqual(self.book2.name, self.form_data['name'])


class TestDeleteBookView(TestCase):

    def setUp(self):
        self.author = baker.make(Author)
        self.client = Client()
        self.book1 = Book.objects.create(name='Book1', author=self.author)
        self.book2 = Book.objects.create(name='Book2', author=self.author)
        self.user = User.objects.create_user(username='mmd', password='1234')
        self.root_user = User.objects.create_superuser(username='root', password='1234')

    def test_deleteBook_view_GET_with_AnonymousUser(self):
        response = self.client.get(reverse('book:deleteBook', args=[self.book1.id]))
        response.user = AnonymousUser()
        self.assertFalse(response.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/account/login/?next=/book/detail/{self.book1.id}/delete/')
        self.assertEqual(Book.objects.count(), 2)

    def test_deleteBook_view_GET_without_staff_user(self):
        self.client.login(username='mmd', password='1234')
        response = self.client.get(reverse('book:deleteBook', args=[self.book1.id]))
        response.user = self.user
        self.assertFalse(response.user.is_staff)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:home'))

    def test_deleteBook_view_with_staff_user_and_invalid_method(self):
        self.client.login(username='root', password='1234')
        response = self.client.post(reverse('book:deleteBook', args=[self.book1.id]))
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:home'))

    def test_deleteBook_view_GET_with_staff_user_and_invalid_id(self):
        self.client.login(username='root', password='1234')
        response = self.client.get(reverse('book:deleteBook', args=[10]))
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Book.objects.count(), 2)

    def test_deleteBook_view_GET_with_staff_user_and_valid_id(self):
        self.client.login(username='root', password='1234')
        response = self.client.get(reverse('book:deleteBook', args=[self.book1.id]))
        response.user = self.root_user
        self.assertTrue(response.user.is_staff)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:home'))
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
        self.assertTrue(Book.objects.filter(id=self.book2.id).exists())


class TestShowBookInstanceView(TestCase):

    def setUp(self):
        self.author = baker.make(Author)
        self.client = Client()
        self.book1 = Book.objects.create(name='Book1', author=self.author)
        self.book2 = Book.objects.create(name='Book2', author=self.author)
        self.user = User.objects.create_user(username='mmd', password='1234')
        self.book_instance = BookInstance.objects.create(book=self.book1, borrower=self.user)

    def test_showBookInstance_GET_with_AnonymousUser(self):
        response = self.client.get(reverse('book:allInstances'))
        response.user = AnonymousUser()
        self.assertFalse(response.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/book/all-instances/')

    def test_showBookInstance_GET_with_user(self):
        self.client.login(username='mmd', password='1234')
        response = self.client.get(reverse('book:allInstances'))
        response.user = self.user
        self.assertTrue(response.user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/showBookInstance.html')
        self.assertContains(response, self.book_instance.book)
        self.assertEqual(response.context['bookInstances'].count(), 1)
        self.assertNotContains(response, self.book2)

    def test_showBookInstance_GET_with_user_and_expired_book_instance(self):
        self.book_instance.due_back = date.today() - timedelta(days=1)
        self.book_instance.save()
        self.client.login(username='mmd', password='1234')
        response = self.client.get(reverse('book:allInstances'))
        response.user = self.user
        self.assertTrue(response.user.is_authenticated)
        self.assertEqual(BookInstance.objects.count(), 0)
        self.assertEqual(self.book1.status, 'a')

    def test_showBookInstance_with_user_and_invalid_method(self):
        self.client.login(username='mmd', password='1234')
        response = self.client.post(reverse('book:allInstances'))
        response.user = self.user
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book:home'))
