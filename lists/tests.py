from django.test import TestCase, Client
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def setUp(self):
        client = Client()

    def test_view_return_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed('home.html')

    def test_save_POST_request(self):
        response = self.client.post('/', {'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redicrect_correctly(self):
        response = self.client.post('/', {'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        
    def test_display_all_list_items(self):
        Item.objects.create(text='Item 1')
        Item.objects.create(text='Item 2')

        response = self.client.get('/')

        self.assertIn('Item 1',response.content.decode())
        self.assertIn('Item 2',response.content.decode())


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

    def test_save_item_only_when_necessery(self):
        client = Client()
        client.get('/')
        self.assertEqual(Item.objects.count(), 0)

