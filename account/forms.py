from django import forms
from .models import Profile
from django.contrib.auth.forms import UserChangeForm
from django.forms import ImageField, FileInput

# form for register user
class RegisterUserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام','id':'sinFirstname'}),max_length = 20, required = True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی','id':'sinLastname'}),max_length = 20, required = True)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام کاربری','id':'sinUsername'}),max_length = 30, required = True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'گذرواژه', 'id':'sinPassword'}), required = True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'تکرار گذرواژه', 'id':'sinPasswordRep'}), required = True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'ایمیل', 'id':'sinEmail'}), required = True)

# form for login user
class LoginUserForm(forms.Form):
    username = forms.CharField(max_length = 20, required = True, widget=forms.TextInput(attrs={'placeholder': 'نام کاربری','id':'userName'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز ورود', 'id':'password'}), required=True)

# for edit user information
class EditUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'disabled': 'disabled',
                                                'id': 'profileNameInput',}),
            'last_name': forms.TextInput(attrs={'disabled': 'disabled',
                                                'id': 'profileLastNameInput',}),
            'email': forms.TextInput(attrs={'disabled': 'disabled',
                                            'id': 'profileEmailInput',}),

        }
    password = None

class EditProfileFrom(forms.ModelForm):
    profileImage= ImageField(widget=FileInput(attrs={
        'class':'profile-img',
        'id':'profile-img',
    }))
    class Meta():
        model = Profile
        fields = ('profileImage',)
        widgets = {
            'profileImage': FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.PNG,.JPG,.JPEG',
                })}