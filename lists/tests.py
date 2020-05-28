from django.test import TestCase, Client
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_view_return_correct_html(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed('home.html')
