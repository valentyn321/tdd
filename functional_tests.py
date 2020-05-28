from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorClass(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=r'/home/valentyn/Documents/tdd-book/code/geckodriver')

    def tearDown(self):
        self.browser.quit()

    def test_main(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-do', header_text)
        self.fail('Finish the test!')  


        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_tag_id('id_new_item')
        self.assertIn(
            inputbox.get_attribute('placeholder'),
            'Enter here, what you have to do...'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_tag_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep
    
if __name__ == '__main__':  
    unittest.main(warnings='ignore')