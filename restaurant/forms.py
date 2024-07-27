from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

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
    new_category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control rounded-input', 'placeholder': 'New Category'})
    )

    class Meta:
        model = Dish
        fields = ['name', 'description', 'ingredients', 'price', 'available', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-input'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control rounded-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control rounded-input'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-control rounded-input'}),
            'category': forms.Select(attrs={'class': 'form-control rounded-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control rounded-input'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control rounded-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-control rounded-input'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control rounded-input'}),
        }

