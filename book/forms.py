from django import forms
from .models import Book, BookInstance
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from datetime import date

class SearchBoxForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ّsearch-box', 'placeholder': 'Search'}),
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
        
    def __init__(self, *args, **kwargs):
        super(AddBookInstanceForm, self).__init__(*args, **kwargs)
        self.fields['due_back'] = JalaliDateField(
            widget = AdminJalaliDateWidget,
            initial=date.today()
            )
        self.fields['due_back'].widget.attrs.update({
            'class': 'jalali_date-date',
            'id': 'mod-date-return'
        })