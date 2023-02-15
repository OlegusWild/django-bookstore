from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import HomePageView, AboutPageView


class HomepageTests(SimpleTestCase):

    # before each test
    def setUp(self) -> None:
        self.url = reverse('home')
        self.homepage_response = self.client.get(self.url)

    def test_homepage_by_client_request(self):
        self.assertEqual(self.url, '/')
        self.assertEqual(self.homepage_response.status_code, 200)
    
    def test_homepage_template_used(self):
        self.assertTemplateUsed(self.homepage_response, 'home.html')
    
    def test_homepage_contains_correct_html_code(self):
        self.assertContains(self.homepage_response, 'Homepage')

    def test_homepage_doesnot_contain_incorrect_html_code(self):
        self.assertNotContains(self.homepage_response, 'Hi, my name is John Doe! I should not be here!')
    
    def test_homepage_url_resolves_homepageview(self):
        url_gives_view = resolve(self.url)
        self.assertEqual(
            url_gives_view.func.__name__,
            HomePageView.as_view().__name__
        )


class AboutPageTests(SimpleTestCase):

    def setUp(self) -> None:
        self.url = reverse('about')
        self.response = self.client.get(self.url)
    
    def test_aboutpage_by_client_request(self):
        self.assertEqual(self.url, '/about/')
        self.assertEqual(self.response.status_code, 200)
    
    def test_aboutpage_template_used(self):
        self.assertTemplateUsed(self.response, 'about.html')
    
    def test_aboutpage_contains_correct_html_code(self):
        self.assertContains(self.response, 'About')

    def test_aboutpage_doesnot_contain_incorrect_html_code(self):
        self.assertNotContains(self.response, 'Hi, my name is John Doe! I should not be here!')
    
    def test_aboutpage_url_resolves_aboutpageview(self):
        url_gives_view = resolve(self.url)
        self.assertEqual(
            url_gives_view.func.__name__,
            AboutPageView.as_view().__name__
        )
