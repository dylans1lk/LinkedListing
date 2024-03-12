import unittest
import app
import json

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, World!', response.data.decode('utf-8'))

    def test_get_all_items(self):
        response = self.app.get('/items')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['items'], list)
        self.assertGreater(len(data['items']), 0)  # Assuming there's at least 1 item

    def test_get_item_valid_id(self):
        response = self.app.get('/items/1')  # Assuming an item with ID 1 exists
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)

    def test_get_item_invalid_id(self):
        response = self.app.get('/items/9999')  # Assuming no item with this ID
        self.assertEqual(response.status_code, 404)

    def test_get_item_string_id(self):
        response = self.app.get('/items/string')  # Invalid ID type
        self.assertEqual(response.status_code, 404)

    # Failing test for CI
  #  def test_home_route(self):
  #      response = self.app.get('/')
  #      self.assertEqual(response.status_code, 404)  # This line is modified to expect a 404 status, causing the test to fail.


if __name__ == '__main__':
    unittest.main()
