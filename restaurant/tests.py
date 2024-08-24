from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from .forms import UserRegisterForm

User = get_user_model()

class UserRegistrationTests(TestCase):
    def test_registration_page_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_registration_form_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'testuser@example.com'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertRedirects(response, reverse('menu'))
    
    def test_registration_form_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'differentpassword',
            'email': 'testuser@example.com'
        })
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response, 'form', 'password2', 'The two password fields must match.')
