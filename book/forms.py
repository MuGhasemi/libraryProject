from django import forms
from .models import Book, BookInstance

class SearchBoxForm(forms.Form):
    search = forms.CharField(
        max_length = 60,
        required = False,) 
    
# --- All Class for Book Instance model ---

class InsertBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = {'name', 'summry', 'genre', 'author', 'bookImage'}
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'add-book-name',
                'type': 'text',
            }),
            'summry': forms.Textarea(attrs={
                'id':'add-book-sumery',
            }),
            'bookImage': forms.FileInput(attrs={
                'id': 'add-book-img',
                'accept': '.jpg,.jpeg,.png,.PNG,.JPG,.JPEG',
                'class':'add-book-img'
            })
        }

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = {'name', 'summry', 'genre', 'author', 'bookImage'}
    
# --- All Class for Book Instance model ---

class AddBookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('due_back',)