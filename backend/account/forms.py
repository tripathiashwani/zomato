from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import password_validation

from .models import User


class SignupForm(UserCreationForm):
    print("forms.py page")
    # user_type=forms.CharField(label='user_type')
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2','user_type')



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name',)