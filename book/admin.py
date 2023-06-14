from django.contrib import admin
from .models import Book, Genre, Author, BookInstance
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'display_genre',
                    'author',
                    'status')
    search_fields = ('name',
                     'author',
                     'genre')
    list_filter = ('author',
                   'genre')
    class Meta:
        ordering = ('genre',)
    
    def display_genre(self, obj):
        return ', '.join([genre.title for genre in obj.genre.all()])
    display_genre.short_description = 'Genre'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',)
    search_fields = ('title',)
    list_filter = ('title',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'last_name',
                    'first_name')
    search_fields = ('last_name',
                     'first_name')
    list_filter = ('last_name',
                   'first_name')
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book',
                    'borrower',
                    'due_back',
                    'status',)
    search_fields = ('book',)
    list_filter = ('due_back',)
    exclude = ('id',)
    