from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import *

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-input',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-input',
            'placeholder': 'Password'
        })
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control rounded-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control rounded-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control rounded-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control rounded-input'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control rounded-input'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control rounded-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control rounded-input'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['contact_info', 'delivery_address', 'payment_method', 'scheduled_time']
        widgets = {
            'contact_info': forms.TextInput(attrs={'class': 'form-control rounded-input'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control rounded-input'}),
            'payment_method': forms.Select(attrs={'class': 'form-control rounded-input'}),
            'scheduled_time': forms.DateTimeInput(attrs={'class': 'form-control rounded-input', 'type': 'datetime-local'}),
        }

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish  # Замість цього використовуйте вашу модель страви
        fields = ['name', 'description', 'price', 'image', 'category']  # Додайте потрібні поля форми
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control rounded-input',
                'placeholder': 'Enter dish name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-input',
                'rows': 5,
                'placeholder': 'Enter dish description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control rounded-input',
                'placeholder': 'Enter price'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control rounded-input',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control rounded-input',
            }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control rounded-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-control rounded-input'}),
        }

from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Замість цього використовуйте вашу модель коментарів
        fields = ['text']  # Додайте потрібні поля форми
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control rounded-input',
                'rows': 5,  # кількість рядків для textarea
                'placeholder': 'Enter your comment here...'
            }),
        }

