# This file contains code for tests specifically relating to
# movie endpoints. Note that these will still need to be called
# from the main test handler.

import json
from tests_misc import *

# *****************************************
# Movie-specific helper functions
# *****************************************

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

# *****************************************
# Top-level tests
# *****************************************

# Test, when reading a movie, that it successfully returns a movie
def test_get_movie(test_obj):
    res = test_obj.client().get('/movies/1')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    test_is_valid_movie(test_obj, data['movie_data'])

def test_get_movie_fail(test_obj):
    res = test_obj.client().get('/movies/100000')
    test_error_format(test_obj, res, 404)

# Test, when reading a movie, that the 
def test_search_movie(test_obj):
    # Use different capitalization in the search to make sure that works
    submission_data = json.dumps(dict(search_term='Movie For Viewing'))
    res = test_obj.client().post('/movies/search',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    test_is_valid_movie_collection(test_obj, data['movie_data'])

def test_search_movie_fail(test_obj):
    # should fail if there is no 'search_term' parameter
    submission_data = json.dumps(dict(bad_search='Movie For Viewing'))
    res_no_parameter = test_obj.client().post('/movies/search',
                                        data=submission_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_no_parameter, 400)
    # should fail if the search term is wrong type
    submission_data = json.dumps(dict(search_term=4))
    res_bad_type = test_obj.client().post('/movies/search',
                                        data=submission_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_bad_type, 400)
    # should fail if there is no data provided
    res_no_data = test_obj.client().post('/movies/search')
    test_error_format(test_obj, res_no_data, 400)

# Test adding a movie, and check that searching back for it retrieves it
def test_add_movie(test_obj):
    submission_data = json.dumps(dict(name='added movie', release_date='2022-01-01'))
    res_submission = test_obj.client().post('/movies',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res_submission.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    test_obj.assertIsInstance(data['id'], int)
    test_obj.assertGreaterEqual(data['id'], 2) # already one entry in the database
    retrieval_data = json.dumps(dict(search_term='added movie'))
    res_retrieval = test_obj.client().post('/movies/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_retrieval, data)
    test_is_valid_movie_collection(test_obj, data['movie_data'])
    test_obj.assertEqual(data['movie_data']['data'][0]['name'], 'added movie')

def test_add_movie_fail(test_obj):
    # should fail if there is no data passed at all
    res_no_data = test_obj.client().post('/movies')
    test_error_format(test_obj, res_no_data, 400)
    # should fail if there is no 'name' parameter
    wrong_type_data = json.dumps(dict(bad_name='2', release_date='2022-01-01'))
    res_wrong_type = test_obj.client().post('/movies',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if 'name' parameter is wrong type
    wrong_type_data = json.dumps(dict(name=2, release_date='2022-01-01'))
    res_wrong_type_name = test_obj.client().post('/movies',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type_name, 400)
    # should fail if 'release_date' parameter is wrong type
    wrong_type_data = json.dumps(dict(name='valid name', release_date=4))
    res_wrong_type_release_date = test_obj.client().post('/movies',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type_release_date, 400)

# Test editing a movie, and check that searching back for the edited movie retrieves it
def test_edit_movie(test_obj):
    # the batch file should have set up a move with id 2 and name 'movie for editing'
    patch_data = json.dumps(dict(name='movie is edited', release_date='2022-01-01'))
    res_patch = test_obj.client().patch('/movies/2',
                                        data=patch_data,
                                        content_type='application/json')
    data = json.loads(res_patch.get_data(as_text=True))
    test_is_success_response(test_obj, res_patch, data)

    # verify move can be found under the new name
    edited_data = json.dumps(dict(search_term='movie is edited'))
    res_edited = test_obj.client().post('/movies/search',
                                        data=edited_data,
                                        content_type='application/json')
    data = json.loads(res_edited.get_data(as_text=True))
    test_is_success_response(test_obj, res_edited, data)
    test_is_valid_movie_collection(test_obj, data['movie_data'])
    test_obj.assertEqual(data['movie_data']['data'][0]['name'], 'movie is edited')

    # Verify original movie name no longer exists
    retrieval_data = json.dumps(dict(search_term='movie for editing'))
    res_retrieval = test_obj.client().post('/movies/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_retrieval, data)
    test_obj.assertEqual(data['movie_data']['count'], 0)
    test_obj.assertEqual(len(data['movie_data']['data']), 0)

def test_edit_movie_fail(test_obj):
    # should fail if there is no data passed at all
    res_no_data = test_obj.client().patch('/movies/1')
    test_error_format(test_obj, res_no_data, 400)
    # should fail if there is no 'name' parameter
    wrong_type_data = json.dumps(dict(bad_name='2', release_date='2022-01-01'))
    res_wrong_type = test_obj.client().patch('/movies/1',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if the 'name' parameter is of the wrong type
    wrong_type_name_data = json.dumps(dict(name=2, release_date='2022-01-01'))
    res_wrong_type_name = test_obj.client().patch('/movies/1',
                                        data=wrong_type_name_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type_name, 400)
    # should fail if the 'release_date' parameter is of the wrong type
    wrong_type_name_data = json.dumps(dict(name='valid name', release_date=2))
    res_wrong_type_name = test_obj.client().patch('/movies/1',
                                        data=wrong_type_name_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type_name, 400)
    # should fail if no movie with correct id is present
    good_data = json.dumps(dict(name='movie for editing', release_date='2022-01-01'))
    res_wrong_type = test_obj.client().patch('/movies/100000',
                                        data=good_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 404)

# Test deleting a movie, and check that searching back for the deleted movie does not return it
def test_delete_movie(test_obj):
    # the batch file should have set up a move with id 3 and name 'movie for editing'
    res_patch = test_obj.client().delete('/movies/3')
    data = json.loads(res_patch.get_data(as_text=True))
    test_is_success_response(test_obj, res_patch, data)

    # Verify original movie name no longer exists
    retrieval_data = json.dumps(dict(search_term='movie for deleting'))
    res_retrieval = test_obj.client().post('/movies/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_retrieval, data)
    test_obj.assertEqual(data['movie_data']['count'], 0)
    test_obj.assertEqual(len(data['movie_data']['data']), 0)

def test_delete_movie_fail(test_obj):
    # should fail if no item with the given id is present
    res_wrong_type = test_obj.client().delete('/movies/100000')
    test_error_format(test_obj, res_wrong_type, 404)