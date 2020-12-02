from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Sign In", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/user-login",
                                  data={"login-email": "test30@test.com",
                                        "login-password": "1234"},
                                  follow_redirects=True)
      
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"account", result.data)



if __name__ == "__main__":
    import unittest

    connect_to_db(app)
    unittest.main()
