from django.test import TestCase
from datetime import date, timedelta
from ..models import Author, Genre, Book, BookInstance
from django.contrib.auth.models import User
from ..forms import (SearchBoxForm,
                     InsertBookForm,
                     EditBookForm,
                     AddBookInstanceForm
                     )

class TestSearchBoxForm(TestCase):

    def test_valid_input(self):
        form = SearchBoxForm(data={'search': 'valid data'})
        self.assertTrue(form.is_valid())


    def test_empty_data(self):
        form = SearchBoxForm(data={})
        self.assertTrue(form.is_valid())

    def test_data_submission(self):
        data = {'search': 'valid data'}
        form = SearchBoxForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['search'], data['search'])

class TestInsertBookForm(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='ali', last_name='akbari')
        self.genre = Genre.objects.create(title='action')
        self.data = {
                    'name': 'book1',
                    'summry': 'summry book1',
                    'genre': [self.genre],
                    'author': self.author,
                    'status': 'a',
                    'bookImage': None,
                    }

    def test_valid_data(self):
        form = InsertBookForm(data=self.data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_empty_data(self):
        form = InsertBookForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_invalid_gener(self):
        form = InsertBookForm(data={
                                'name': 'book1',
                                'summry': 'summry book1',
                                'genre': [2],
                                'author': self.author.id,
                                'status': 'a',
                                'bookImage': None,
                                })
        self.assertEqual(len(form.errors), 1)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('genre'))

    def test_data_submission(self):
        form = InsertBookForm(data=self.data)
        self.assertTrue(form.is_valid())
        book = form.save()
        self.assertEqual(book.name, self.data['name'])
        self.assertEqual(book.summry, self.data['summry'])
        self.assertEqual(book.genre.first(), self.genre)
        self.assertEqual(book.genre.count(), 1)
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.status, self.data['status'])
        self.assertEqual(book.bookImage, self.data['bookImage'])


class TestEditBookForm(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='ali', last_name='akbari')
        self.genre = Genre.objects.create(title='action')
        self.book = Book.objects.create(
            name='book1',
            summry='summary book1',
            author=self.author,
            status='a',
        )
        self.book.genre.add(self.genre)
        self.form_data = {
            'name': 'book1 updated',
            'summry': 'summary book1 updated',
            'genre': [self.genre.id],
            'author': self.author.id,
            'bookImage': None,
        }

    def test_valid_data(self):
        form = EditBookForm(data=self.form_data, instance=self.book)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)


    def test_empty_data(self):
        form = EditBookForm(data={}, instance=self.book)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_data_submission(self):
        form = EditBookForm(data=self.form_data, instance=self.book)
        self.assertTrue(form.is_valid())
        updated_book = form.save()
        self.assertEqual(updated_book.name, 'book1 updated')
        self.assertEqual(updated_book.summry, 'summary book1 updated')
        self.assertEqual(updated_book.genre.first(), self.genre)
        self.assertEqual(updated_book.genre.count(), 1)
        self.assertEqual(updated_book.author, self.author)
        self.assertEqual(updated_book.status, 'a')
        self.assertEqual(updated_book.bookImage, None)


class TestAddBookInstanceFrom(TestCase):

    def test_initial_data(self):
        form = AddBookInstanceForm()
        self.assertEqual(form.fields['due_back'].initial, date.today())

    def test_valid_date(self):
        form = AddBookInstanceForm(data={'due_back':'1402-08-29'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['due_back'], date(2023, 11, 20))