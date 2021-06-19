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

# Test that the response matches the expected format for the given error code
def test_error_format(test_obj, res, code):
    data = json.loads(res.get_data(as_text=True))
    test_obj.assertEqual(res.status_code, code)
    test_obj.assertFalse(data['success'])
    test_obj.assertIsInstance(data['error'], int)
    test_obj.assertEqual(data['error'], code)
    test_obj.assertIsInstance(data['message'], str)
    test_obj.assertEqual(data['message'], error_names[code])

def test_is_success_response(test_obj, res, data=None):
    if data is None: data = json.loads(res.get_data(as_text=True))
    test_obj.assertEqual(res.status_code, 200)
    test_obj.assertTrue(data['success'])

# Test that this object "obj" is in fact a valid representation of a movie
def test_is_valid_movie(test_obj, obj):
    test_obj.assertIsInstance(obj, object)
    test_obj.assertIsInstance(obj['id'], int)
    test_obj.assertGreaterEqual(obj['id'], 1)
    test_obj.assertIsInstance(obj['name'], str)
    test_obj.assertGreaterEqual(len(obj['name']), 1)
    test_obj.assertIsInstance(obj['release_date'], str)
    test_obj.assertGreaterEqual(len(obj['release_date']), 1)

# Test that this object "obj" is in fact a valid representation of a movie list
# (it will be an object, not actually a list itself)
def test_is_valid_movie_collection(test_obj, obj):
    test_obj.assertIsInstance(obj, object)
    test_obj.assertIsInstance(obj['count'], int)
    test_obj.assertGreaterEqual(obj['count'], 1)
    test_obj.assertIsInstance(obj['data'], list)
    test_obj.assertGreaterEqual(len(obj['data']), 1)
    for data_item in obj['data']:
        test_is_valid_movie(test_obj, data_item)

def get_id_for_movie(test_obj, movie_title):
    retrieval_data = json.dumps(dict(search_term=movie_title))
    res = test_obj.client().post('/movies/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    return data['movie_data']['data'][0]['id']

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

    # Test, when reading a movie, that it successfully returns a movie
    def test_get_movie(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.get_data(as_text=True))
        test_is_success_response(self, res, data)
        test_is_valid_movie(self, data['movie_data'])

    def test_get_movie_fail(self):
        res = self.client().get('/movies/100000')
        test_error_format(self, res, 404)

    # Test, when reading a movie, that the 
    def test_search_movie(self):
        # Use different capitalization in the search to make sure that works
        submission_data = json.dumps(dict(search_term='Test Name'))
        res = self.client().post('/movies/search',
                                            data=submission_data,
                                            content_type='application/json')
        data = json.loads(res.get_data(as_text=True))
        test_is_success_response(self, res, data)
        test_is_valid_movie_collection(self, data['movie_data'])

    # Test adding a movie, and check that searching back for it retrieves it
    def test_add_movie(self):
        submission_data = json.dumps(dict(name='added movie'))
        res_submission = self.client().post('/movies',
                                            data=submission_data,
                                            content_type='application/json')
        data = json.loads(res_submission.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)
        retrieval_data = json.dumps(dict(search_term='added movie'))
        res_retrieval = self.client().post('/movies/search',
                                            data=retrieval_data,
                                            content_type='application/json')
        data = json.loads(res_retrieval.get_data(as_text=True))
        test_is_success_response(self, res_retrieval, data)
        test_is_valid_movie_collection(self, data['movie_data'])
        self.assertEqual(data['movie_data']['data'][0]['name'], 'added movie')

    def test_add_movie_fail(self):
        # should fail if there is no data passed at all
        res_no_data = self.client().post('/movies')
        test_error_format(self, res_no_data, 400)
        # should fail if there is no 'name' parameter
        wrong_type_data = json.dumps(dict(bad_name='2'))
        res_wrong_type = self.client().post('/movies',
                                            data=wrong_type_data,
                                            content_type='application/json')
        test_error_format(self, res_wrong_type, 400)
        # should fail if 'name' parameter is wrong type
        wrong_type_data = json.dumps(dict(name=2))
        res_wrong_type = self.client().post('/movies',
                                            data=wrong_type_data,
                                            content_type='application/json')
        test_error_format(self, res_wrong_type, 400)

    # Test adding a movie, editing it, and check that searching back for the edited movie retrieves it
    def test_edit_movie(self):
        # post a specific movie to patch
        submission_data = json.dumps(dict(name='movie for editing'))
        res_submission = self.client().post('/movies',
                                            data=submission_data,
                                            content_type='application/json')
        data = json.loads(res_submission.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)

        # need to get the id for the created movie
        item_id = get_id_for_movie(self, 'movie for editing')

        # use the id to patch the movie
        patch_data = json.dumps(dict(name='movie is edited'))
        res_patch = self.client().patch('/movies/' + str(item_id),
                                            data=patch_data,
                                            content_type='application/json')
        data = json.loads(res_patch.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)

        # verify move can be found under the new name
        edited_data = json.dumps(dict(search_term='movie is edited'))
        res_edited = self.client().post('/movies/search',
                                            data=edited_data,
                                            content_type='application/json')
        data = json.loads(res_edited.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)
        test_is_valid_movie_collection(self, data['movie_data'])
        self.assertEqual(data['movie_data']['data'][0]['name'], 'movie is edited')

        # Verify original movie name no longer exists
        retrieval_data = json.dumps(dict(search_term='movie for editing'))
        res_retrieval = self.client().post('/movies/search',
                                            data=retrieval_data,
                                            content_type='application/json')
        data = json.loads(res_retrieval.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)
        self.assertEqual(data['movie_data']['count'], 0)
        self.assertEqual(len(data['movie_data']['data']), 0)

    def test_edit_movie_fail(self):
        # should fail if there is no data passed at all
        res_no_data = self.client().patch('/movies/1')
        test_error_format(self, res_no_data, 400)
        # should fail if there is no 'name' parameter
        wrong_type_data = json.dumps(dict(bad_name='2'))
        res_wrong_type = self.client().patch('/movies/1',
                                            data=wrong_type_data,
                                            content_type='application/json')
        test_error_format(self, res_wrong_type, 400)
        # should fail if there is no 'name' parameter
        wrong_type_data = json.dumps(dict(name=2))
        res_wrong_type = self.client().patch('/movies/1',
                                            data=wrong_type_data,
                                            content_type='application/json')
        test_error_format(self, res_wrong_type, 400)
        # should fail if no movie with correct id is present
        good_data = json.dumps(dict(name='movie for editing'))
        res_wrong_type = self.client().patch('/movies/100000',
                                            data=good_data,
                                            content_type='application/json')
        test_error_format(self, res_wrong_type, 404)

    # Test adding a movie, deleting it, and check that searching back for the deleted movie does not return it
    def test_delete_movie(self):
        # post a specific movie to delete
        submission_data = json.dumps(dict(name='movie for deleting'))
        res_submission = self.client().post('/movies',
                                            data=submission_data,
                                            content_type='application/json')
        data = json.loads(res_submission.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)

        # need to get the id for the created movie
        item_id = get_id_for_movie(self, 'movie for deleting')

        # delete the movie at the given id
        res_patch = self.client().delete('/movies/' + str(item_id))
        data = json.loads(res_patch.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)

        # Verify original movie name no longer exists
        retrieval_data = json.dumps(dict(search_term='movie for deleting'))
        res_retrieval = self.client().post('/movies/search',
                                            data=retrieval_data,
                                            content_type='application/json')
        data = json.loads(res_retrieval.get_data(as_text=True))
        test_is_success_response(self, res_submission, data)
        self.assertEqual(data['movie_data']['count'], 0)
        self.assertEqual(len(data['movie_data']['data']), 0)
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    app.run()