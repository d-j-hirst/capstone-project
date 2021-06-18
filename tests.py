import unittest
import json
import os
import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import database_path

# Get the database path from an environment variable
# Heroku automatically generates a DATABASE_URL beginning with
#  "postgres://" (which can't be easily edited), while SQLAlchemy in
#  its latest version will only work with "postgresql://". This
#  adjustment allows compatibility between the two by converting
#  the scheme of Heroku's URL
database_path = os.environ.get('DATABASE_URL').replace("s://", "sql://", 1)
# replace the database name with this to run the tests - we don't want to
# overwrite persistent data in the regular database
database_path = database_path.rsplit('/', 1)[0] + '/capstone_test_db'


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

    # Define test variables and initialize app.
    def setUp(self):
        self.app = create_app({'database_path': database_path})
        self.client = self.app.test_client

    # Executed after each test
    def tearDown(self):
        pass

    # Test that successful tests actually work
    def test_test(self):
        self.assertEqual(200, 200)

    # Test trivial I/O to make sure the server is responding
    def test_index(self):
        res = self.client().get('/test')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Test, when reading a movie, that the 
    def test_get_movie(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie_data'], object)
        self.assertIsInstance(data['movie_data']['id'], int)
        self.assertGreaterEqual(data['movie_data']['id'], 1)
        self.assertIsInstance(data['movie_data']['name'], str)
        self.assertGreaterEqual(len(data['movie_data']['name']), 1)
        self.assertIsInstance(data['movie_data']['release_date'], str)

    # Test, when reading a movie, that the 
    def test_search_movie(self):
        # Use different capitalization in the search to make sure that works
        submission_data = json.dumps(dict(search_term='Test Name'))
        res = self.client().post('/movies/search',
                                            data=submission_data,
                                            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['movie_data'], object)
        self.assertIsInstance(data['movie_data']['count'], int)
        self.assertGreaterEqual(data['movie_data']['count'], 1)
        self.assertIsInstance(data['movie_data']['data'], list)
        self.assertGreaterEqual(len(data['movie_data']['data']), 1)
        self.assertIsInstance(data['movie_data']['data'][0], object)
        self.assertIsInstance(data['movie_data']['data'][0]['id'], int)
        self.assertGreaterEqual(data['movie_data']['data'][0]['id'], 1)
        self.assertIsInstance(data['movie_data']['data'][0]['name'], str)
        self.assertGreaterEqual(len(data['movie_data']['data'][0]['name']), 9)
        self.assertIsInstance(data['movie_data']['data'][0]['release_date'], str)
        self.assertGreaterEqual(len(data['movie_data']['data'][0]['release_date']), 1)

    # Test adding a movie
    def test_add_movie(self):
        submission_data = json.dumps(dict(name='test name'))
        res_submission = self.client().post('/movies',
                                            data=submission_data,
                                            content_type='application/json')
        data = json.loads(res_submission.get_data(as_text=True))
        self.assertEqual(res_submission.status_code, 200)
        self.assertTrue(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    app.run()