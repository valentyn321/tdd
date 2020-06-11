from django.test import TestCase, Client
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def setUp(self):
        client = Client()

    def test_view_return_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed('home.html')

class ListAndItemModelTest(TestCase):
    
    def test_saving_and_returning_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "First_item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Second_item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        qs = Item.objects.all()
        self.assertEqual(qs.count(), 2)

        first_item_from_qs = qs[0]
        second_item_from_qs = qs[1]
        self.assertEqual(first_item_from_qs.text, 'First_item')
        self.assertEqual(first_item_from_qs.list, list_)
        self.assertEqual(second_item_from_qs.text, 'Second_item')
        self.assertEqual(second_item_from_qs.list, list_)

class ListViewTest(TestCase): 

    def setUp(self):
        client = Client()

    def test_display_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Item 1')
        Item.objects.create(list=list_, text='Item 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):
    
    def test_save_POST_request(self):
        response = self.client.post('/lists/new', {'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redicrect_correctly(self):
        response = self.client.post('/lists/new', {'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')