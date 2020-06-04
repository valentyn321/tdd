from django.test import TestCase, Client
from lists.views import home_page
from lists.models import Item


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


class ItemModelTest(TestCase):
    
    def test_saving_and_returning_items(self):
        first_item = Item()
        first_item.text = "First_item"
        first_item.save()

        second_item = Item()
        second_item.text = "Second_item"
        second_item.save()

        qs = Item.objects.all()
        self.assertEqual(qs.count(), 2)

        first_item_from_qs = qs[0]
        second_item_from_qs = qs[1]
        self.assertEqual(first_item_from_qs.text, 'First_item')
        self.assertEqual(second_item_from_qs.text, 'Second_item')

