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

    def test_display_items_for_that_lists(self):
        correct_list = List.objects.create()
        Item.objects.create(list=correct_list, text='Item 1')
        Item.objects.create(list=correct_list, text='Item 2')
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text='Item 1(other list)')
        Item.objects.create(list=other_list, text='Item 1(other list)')

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertNotContains(response, 'Item 1(other list)')
        self.assertNotContains(response, 'Item 2(other list)')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):
    
    def test_save_POST_request(self):
        response = self.client.post('/lists/new', {'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redicrect_correctly(self):
        response = self.client.post('/lists/new', {'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')