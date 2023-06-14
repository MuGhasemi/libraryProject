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
        fields = '__all__'

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
    
# --- All Class for Book Instance model ---

class AddBookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('due_back',)