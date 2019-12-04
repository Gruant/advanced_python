import unittest
from app.user import User


class TestVKinderData(unittest.TestCase):
    def setUp(self):
        self.user = User(id)
        self.user.groups = [47348, 5656, 65343, 55454]

    def tearDown(self):
        pass

    def test__init(self):
        with self.assertRaises(TypeError):
            self.user = User()
            self.user = User('544454')
            self.user = User(43343)

    def take_list(self):
        search_list = self.user.search_all()
        self.assertTrue(type(search_list) == list)


if __name__ == '__main__':
    unittest.main()