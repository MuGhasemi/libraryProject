from django.test import TestCase
from ..views import (home,
                     addBook,
                     detail,
                     editBook,
                     deleteBook,
                     showGenres,
                     showAuthors,
                     showBookInstance
                     )
from django.urls import resolve, reverse


class TestUrl(TestCase):

    def test_home_url(self):
        url = reverse('book:home')
        self.assertEqual(resolve(url).func, home)

    def test_addBook_url(self):
        url = reverse('book:addBook')
        self.assertEqual(resolve(url).func, addBook)

    def test_detail_url(self):
        url = reverse('book:detail', args=[1])
        self.assertEqual(resolve(url).func, detail)

    def test_editBook_url(self):
        url = reverse('book:editBook', args=[1])
        self.assertEqual(resolve(url).func, editBook)

    def test_deleteBook_url(self):
        url = reverse('book:deleteBook', args=[1])
        self.assertEqual(resolve(url).func, deleteBook)

    def test_showGenres_url(self):
        url = reverse('book:allGenres')
        self.assertEqual(resolve(url).func, showGenres)

    def test_showAuthors_url(self):
        url = reverse('book:allAuthors')
        self.assertEqual(resolve(url).func, showAuthors)

    def test_showBookInstance_url(self):
        url = reverse('book:allInstances')
        self.assertEqual(resolve(url).func, showBookInstance)

