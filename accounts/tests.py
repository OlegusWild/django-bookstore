from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .views import SignUpPageView
from .forms import UserCreationForm


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignUpTests(TestCase):

    def setUp(self) -> None:
        self.url = reverse('signup')
        self.signup_page = self.client.get(self.url)
    
    def test_signup_template(self):
        self.assertEqual(self.url, '/accounts/signup/')

        self.assertEqual(self.signup_page.status_code, 200)

        self.assertTemplateUsed(self.signup_page, 'registration/signup.html')

        self.assertContains(self.signup_page, 'Sign Up')
        self.assertNotContains(self.signup_page, 'Incorrect thing ;)')

    def test_signup_view(self):
        url_gives_view = resolve(self.url)
        self.assertEqual(
            url_gives_view.func.__name__,
            SignUpPageView.as_view().__name__
        )
    
    def test_signup_form(self):
        form_obj = self.signup_page.context.get('form')
        self.assertIsInstance(
            form_obj,
            UserCreationForm
        )