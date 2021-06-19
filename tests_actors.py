# This file contains code for tests specifically relating to
# actor endpoints. Note that these will still need to be called
# from the main test handler.

import json
from tests_misc import *

# *****************************************
# Actor-specific helper functions
# *****************************************

# Test that this object "obj" is in fact a valid representation of a actor
def test_is_valid_actor(test_obj, obj):
    test_obj.assertIsInstance(obj, object)
    test_obj.assertIsInstance(obj['id'], int)
    test_obj.assertGreaterEqual(obj['id'], 1)
    test_obj.assertIsInstance(obj['name'], str)
    test_obj.assertGreaterEqual(len(obj['name']), 1)
    test_obj.assertIsInstance(obj['age'], int)
    test_obj.assertGreaterEqual(obj['age'], 0)
    test_obj.assertIsInstance(obj['gender'], str)
    test_obj.assertGreaterEqual(len(obj['gender']), 1)

# Test that this object "obj" is in fact a valid representation of a actor list
# (it will be an object, not actually a list itself)
def test_is_valid_actor_collection(test_obj, obj):
    test_obj.assertIsInstance(obj, object)
    test_obj.assertIsInstance(obj['count'], int)
    test_obj.assertGreaterEqual(obj['count'], 1)
    test_obj.assertIsInstance(obj['data'], list)
    test_obj.assertGreaterEqual(len(obj['data']), 1)
    for data_item in obj['data']:
        test_is_valid_actor(test_obj, data_item)

def get_id_for_actor(test_obj, actor_title):
    retrieval_data = json.dumps(dict(search_term=actor_title))
    res = test_obj.client().post('/actors/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    return data['actor_data']['data'][0]['id']

# *****************************************
# Top-level tests
# *****************************************

# Test, when reading a actor, that it successfully returns a actor
def test_get_actor(test_obj):
    res = test_obj.client().get('/actors/1')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    test_is_valid_actor(test_obj, data['actor_data'])

def test_get_actor_fail(test_obj):
    res = test_obj.client().get('/actors/100000')
    test_error_format(test_obj, res, 404)

# Test, when reading a actor, that the 
def test_search_actor(test_obj):
    # Use different capitalization in the search to make sure that works
    submission_data = json.dumps(dict(search_term='Test Name'))
    res = test_obj.client().post('/actors/search',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res.get_data(as_text=True))
    test_is_success_response(test_obj, res, data)
    test_is_valid_actor_collection(test_obj, data['actor_data'])

# Test adding a actor, and check that searching back for it retrieves it
def test_add_actor(test_obj):
    submission_data = json.dumps(dict(name='added actor', age=26, gender='gender'))
    res_submission = test_obj.client().post('/actors',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res_submission.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    retrieval_data = json.dumps(dict(search_term='added actor'))
    res_retrieval = test_obj.client().post('/actors/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_retrieval, data)
    test_is_valid_actor_collection(test_obj, data['actor_data'])
    test_obj.assertEqual(data['actor_data']['data'][0]['name'], 'added actor')

def test_add_actor_fail(test_obj):
    # should fail if there is no data passed at all
    res_no_data = test_obj.client().post('/actors')
    test_error_format(test_obj, res_no_data, 400)
    # should fail if there is no 'name' parameter
    wrong_type_data = json.dumps(dict(bad_name='2'))
    res_wrong_type = test_obj.client().post('/actors',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if 'name' parameter is wrong type
    wrong_type_data = json.dumps(dict(name=2, age=26, gender='gender'))
    res_wrong_type = test_obj.client().post('/actors',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)

# Test adding a actor, editing it, and check that searching back for the edited actor retrieves it
def test_edit_actor(test_obj):
    # post a specific actor to patch
    submission_data = json.dumps(dict(name='actor for editing', age=26, gender='gender'))
    res_submission = test_obj.client().post('/actors',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res_submission.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # need to get the id for the created actor
    item_id = get_id_for_actor(test_obj, 'actor for editing')

    # use the id to patch the actor
    patch_data = json.dumps(dict(name='actor is edited', age=26, gender='gender'))
    res_patch = test_obj.client().patch('/actors/' + str(item_id),
                                        data=patch_data,
                                        content_type='application/json')
    data = json.loads(res_patch.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # verify move can be found under the new name
    edited_data = json.dumps(dict(search_term='actor is edited'))
    res_edited = test_obj.client().post('/actors/search',
                                        data=edited_data,
                                        content_type='application/json')
    data = json.loads(res_edited.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    test_is_valid_actor_collection(test_obj, data['actor_data'])
    test_obj.assertEqual(data['actor_data']['data'][0]['name'], 'actor is edited')

    # Verify original actor name no longer exists
    retrieval_data = json.dumps(dict(search_term='actor for editing'))
    res_retrieval = test_obj.client().post('/actors/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    test_obj.assertEqual(data['actor_data']['count'], 0)
    test_obj.assertEqual(len(data['actor_data']['data']), 0)

def test_edit_actor_fail(test_obj):
    # should fail if there is no data passed at all
    res_no_data = test_obj.client().patch('/actors/1')
    test_error_format(test_obj, res_no_data, 400)
    # should fail if there is no 'name' parameter
    wrong_type_data = json.dumps(dict(bad_name='2'))
    res_wrong_type = test_obj.client().patch('/actors/1',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if there is no 'name' parameter
    wrong_type_data = json.dumps(dict(name=2))
    res_wrong_type = test_obj.client().patch('/actors/1',
                                        data=wrong_type_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 400)
    # should fail if no actor with correct id is present
    good_data = json.dumps(dict(name='actor for editing', age=26, gender='gender'))
    res_wrong_type = test_obj.client().patch('/actors/100000',
                                        data=good_data,
                                        content_type='application/json')
    test_error_format(test_obj, res_wrong_type, 404)

# Test adding a actor, deleting it, and check that searching back for the deleted actor does not return it
def test_delete_actor(test_obj):
    # post a specific actor to delete
    submission_data = json.dumps(dict(name='actor for deleting', age=26, gender='gender'))
    res_submission = test_obj.client().post('/actors',
                                        data=submission_data,
                                        content_type='application/json')
    data = json.loads(res_submission.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # need to get the id for the created actor
    item_id = get_id_for_actor(test_obj, 'actor for deleting')

    # delete the actor at the given id
    res_patch = test_obj.client().delete('/actors/' + str(item_id))
    data = json.loads(res_patch.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)

    # Verify original actor name no longer exists
    retrieval_data = json.dumps(dict(search_term='actor for deleting'))
    res_retrieval = test_obj.client().post('/actors/search',
                                        data=retrieval_data,
                                        content_type='application/json')
    data = json.loads(res_retrieval.get_data(as_text=True))
    test_is_success_response(test_obj, res_submission, data)
    test_obj.assertEqual(data['actor_data']['count'], 0)
    test_obj.assertEqual(len(data['actor_data']['data']), 0)

def test_delete_actor_fail(test_obj):
    # should fail if no item with the given id is present
    res_wrong_type = test_obj.client().delete('/actors/100000')
    test_error_format(test_obj, res_wrong_type, 404)