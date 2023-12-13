from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-3 px-4 rounded-xl'
    }))

    email = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': 'Your email',
        'class': 'w-full py-3 px-4 rounded-xl'
    }))

    password1 = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-3 px-4 rounded-xl'
    }))

    password2 = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': 'Your password again',
        'class': 'w-full py-3 px-4 rounded-xl'
    }))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-3 px-4 rounded-xl'
    }))

    password = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-3 px-4 rounded-xl'
    }))