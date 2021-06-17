import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


error_names = {400: 'Bad Request',
               401: 'Unauthorized',
               403: 'Forbidden',
               404: 'Not Found',
               422: 'Unprocessable Entity',
               500: 'Internal Server Error'}


def test_error_format(test_obj, res, code):
    data = json.loads(res.get_data(as_text=True))
    test_obj.assertEqual(res.status_code, code)
    test_obj.assertFalse(data['success'])
    test_obj.assertIsInstance(data['error'], int)
    test_obj.assertEqual(data['error'], code)
    test_obj.assertIsInstance(data['message'], str)
    test_obj.assertEqual(data['message'], error_names[code])


class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_test(self):
        """Test that successful tests actually work"""
        self.assertEqual(200, 200)

    def test_index(self):
        res = self.client().get('/test')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    app.run()