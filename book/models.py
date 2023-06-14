import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

# Create your models here.

class Genre(models.Model):
    title = models.CharField(max_length = 60,
                             help_text = 'Enter a book genre (e.g. Science Fiction, French poetry etc.)')
    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length = 60,
                                  null = False,
                                  blank = False,)
    last_name = models.CharField(max_length = 60,
                                 null = False,
                                 blank = False,)
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Book(models.Model):
    LOAN_STATUS = (
                    ('o', 'On Loan'),
                    ('a', 'Available'),
                   )
    name = models.CharField(max_length = 60,
                            null = False,
                            blank = False,)
    summry = models.TextField(max_length = 1000,
                              help_text = 'Enter a brief description of the book')
    genre = models.ManyToManyField(Genre,
                                   help_text = 'Select a genre for this book')
    author = models.ForeignKey('Author',
                               on_delete = models.PROTECT,
                               null = False,)
    status = models.CharField(max_length = 1,
                              choices = LOAN_STATUS,
                              default = 'a',
                              blank = False,
                              null = False)
    def __str__(self):
        return self.name

class BookInstance(models.Model):
    LOAN_STATUS = (
                    ('o', 'On Loan'),
                    ('a', 'Available'),
                   )
    TODAY = datetime.today()
    DUE_DATE = TODAY + timedelta(weeks = 1)

    def default_user():
        return get_user_model().objects.filter(username = get_user_model().__name__)
    
    id = models.UUIDField(primary_key = True,
                          default = uuid.uuid1,
                          help_text = 'Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book,
                             on_delete = models.PROTECT,
                             null = False,
                             blank = False,)
    due_back = models.DateField(default = DUE_DATE,
                                null = False,
                                blank = False,
                                help_text = 'Default one week (7days).')
    borrower = models.ForeignKey(User,
                                 on_delete = models.PROTECT,
                                 null = False,
                                 blank = False,)
    status = models.CharField(max_length = 1,
                              choices = LOAN_STATUS,
                              default = 'o',
                              blank = False,
                              null = False)
    class Meta:
        ordering = ["due_back"]
        verbose_name = 'Book Instance'
    
    def __str__(self):
        return f"{self.borrower}, {self.book}"