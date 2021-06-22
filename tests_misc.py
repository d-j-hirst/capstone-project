# This file contains miscellanous testing methods for widespread use
# across different parts of the program

import json

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
    if data is None:
        data = json.loads(res.get_data(as_text=True))
    test_obj.assertEqual(res.status_code, 200)
    test_obj.assertTrue(data['success'])
