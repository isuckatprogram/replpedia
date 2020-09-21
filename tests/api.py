import requests
import unittest


class TestAPI(unittest.TestCase):

  def test_search(self):
    b = requests.post('https://replpedia.jdaniels.me/api/search', json={'search': 'test'})

    json = b.json()
    self.assertEqual(json['ok'], True, "The search API isn't working! Is your code correct?")


if __name__ == '__main__':
  unittest.main()