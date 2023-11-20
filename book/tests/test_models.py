from django.test import TestCase
from ..models import Genre, Author, Book, BookInstance
from django.contrib.auth.models import User
from model_bakery import baker


class TestGenreModel(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(title='action')

    def test_model_str(self):
        self.assertEqual(str(self.genre), 'action')

class TestAuthorModel(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name='mmd', last_name='ghasemi')

    def test_model_str(self):
        self.assertEqual(str(self.author), 'ghasemi, mmd')


class TestBookModel(TestCase):

    def setUp(self):
        self.book = baker.make(Book, name='book1')

    def test_model_str(self):
        self.assertEqual(str(self.book), 'book1')


class TestBookInstanceModel(TestCase):

    def setUp(self):
        self.book = baker.make(Book, name='book1')
        self.user = baker.make(User, username='mmd')
        self.instance = baker.make(BookInstance, borrower=self.user, book=self.book)

    def test_model_str(self):
        self.assertEqual(str(self.instance), 'mmd, book1')