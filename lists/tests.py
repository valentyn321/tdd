from django.test import TestCase, Client
from lists.views import home_page


class HomePageTest(TestCase):

    def test_view_return_correct_html(self):
        client = Client()
        response = client.get('/')
        self.assertTemplateUsed('home.html')

    def test_save_POST_request(self):
        client = Client()
        response = client.post('/', {'item_text': 'A new list item'})
        self.assertIn("A new list item", response.content.decode())
        self.assertTemplateUsed(response, 'home.html')