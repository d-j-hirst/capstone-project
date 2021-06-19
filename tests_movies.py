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

def get_id_for_movie(test_obj, movie_title):
    retrieval_data = json.dumps(dict(search_term=movie_title))
    res = test_obj.client().post('/movies/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    return data['movie_data']['data'][0]['id']

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
    submission_data = json.dumps(dict(search_term='Test Name'))
    res = test_obj.client().post('/movies/search',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    test_is_valid_movie_collection(test_obj, data['movie_data'])

# Test adding a movie, and check that searching back for it retrieves it
def test_add_movie(test_obj):
    submission_data = json.dumps(dict(name='added movie'))
    res_submission = test_obj.client().post('/movies',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res_submission.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
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
    wrong_type_data = json.dumps(dict(bad_name='2'))
    res_wrong_type = test_obj.client().post('/movies',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if 'name' parameter is wrong type
    wrong_type_data = json.dumps(dict(name=2))
    res_wrong_type = test_obj.client().post('/movies',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)

# Test adding a movie, editing it, and check that searching back for the edited movie retrieves it
def test_edit_movie(test_obj):
    # post a specific movie to patch
    submission_data = json.dumps(dict(name='movie for editing'))
    res_submission = test_obj.client().post('/movies',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res_submission.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # need to get the id for the created movie
    item_id = get_id_for_movie(test_obj, 'movie for editing')

    # use the id to patch the movie
    patch_data = json.dumps(dict(name='movie is edited'))
    res_patch = test_obj.client().patch('/movies/' + str(item_id),
                                        data=patch_data,
                                        content_type='application/json')
    data = json.loads(res_patch.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # verify move can be found under the new name
    edited_data = json.dumps(dict(search_term='movie is edited'))
    res_edited = test_obj.client().post('/movies/search',
                                        data=edited_data,
                                        content_type='application/json')
    data = json.loads(res_edited.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    test_is_valid_movie_collection(test_obj, data['movie_data'])
    test_obj.assertEqual(data['movie_data']['data'][0]['name'], 'movie is edited')

    # Verify original movie name no longer exists
    retrieval_data = json.dumps(dict(search_term='movie for editing'))
    res_retrieval = test_obj.client().post('/movies/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    test_obj.assertEqual(data['movie_data']['count'], 0)
    test_obj.assertEqual(len(data['movie_data']['data']), 0)

def test_edit_movie_fail(test_obj):
    # should fail if there is no data passed at all
    res_no_data = test_obj.client().patch('/movies/1')
    test_error_format(test_obj, res_no_data, 400)
    # should fail if there is no 'name' parameter
    wrong_type_data = json.dumps(dict(bad_name='2'))
    res_wrong_type = test_obj.client().patch('/movies/1',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if there is no 'name' parameter
    wrong_type_data = json.dumps(dict(name=2))
    res_wrong_type = test_obj.client().patch('/movies/1',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if no movie with correct id is present
    good_data = json.dumps(dict(name='movie for editing'))
    res_wrong_type = test_obj.client().patch('/movies/100000',
                                        data=good_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 404)

# Test adding a movie, deleting it, and check that searching back for the deleted movie does not return it
def test_delete_movie(test_obj):
    # post a specific movie to delete
    submission_data = json.dumps(dict(name='movie for deleting'))
    res_submission = test_obj.client().post('/movies',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res_submission.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # need to get the id for the created movie
    item_id = get_id_for_movie(test_obj, 'movie for deleting')

    # delete the movie at the given id
    res_patch = test_obj.client().delete('/movies/' + str(item_id))
    data = json.loads(res_patch.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # Verify original movie name no longer exists
    retrieval_data = json.dumps(dict(search_term='movie for deleting'))
    res_retrieval = test_obj.client().post('/movies/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    test_obj.assertEqual(data['movie_data']['count'], 0)
    test_obj.assertEqual(len(data['movie_data']['data']), 0)

def test_delete_movie_fail(test_obj):
    # should fail if no item with the given id is present
    res_wrong_type = test_obj.client().delete('/movies/100000')
    test_error_format(test_obj, res_wrong_type, 404)