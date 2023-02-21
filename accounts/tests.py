from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve


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
    username = 'newuser'
    email = 'test@email.com'

    def setUp(self) -> None:
        self.url = reverse('account_signup')
        self.signup_page = self.client.get(self.url)
    
    def test_signup_template(self):
        self.assertEqual(self.url, '/accounts/signup/')

        self.assertEqual(self.signup_page.status_code, 200)

        self.assertTemplateUsed(self.signup_page, 'account/signup.html')

        self.assertContains(self.signup_page, 'Sign Up')
        self.assertNotContains(self.signup_page, 'Incorrect thing ;)')

    def test_signup_form(self):
        _new_user = get_user_model().objects.create_user(self.username, self.email)

        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
            [0].username, self.username)
        self.assertEqual(get_user_model().objects.all()
            [0].email, self.email)
