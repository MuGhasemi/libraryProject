from django import forms
from .models import Profile


# form for register user
class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length = 20, required = True)
    last_name = forms.CharField(max_length = 20, required = True)
    username = forms.CharField(max_length = 30, required = True)
    password = forms.CharField(widget = forms.PasswordInput, required = True)
    email = forms.CharField(widget = forms.EmailInput, required = True)

# form for login user

class LoginUserForm(forms.Form):
    username = forms.CharField(max_length = 20, required = True)
    password = forms.CharField(widget = forms.PasswordInput, required = True)