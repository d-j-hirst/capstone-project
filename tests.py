import unittest
import json
import os
import datetime
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import database_path
from tests_misc import *
from tests_movies import *

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

    def test_get_movie(self):
        test_get_movie(self)

    def test_get_movie_fail(self):
        test_get_movie_fail(self)

    def test_search_movie(self):
        test_search_movie(self)

    def test_add_movie(self):
        test_add_movie(self)

    def test_add_movie_fail(self):
        test_add_movie_fail(self)

    def test_edit_movie(self):
        test_edit_movie(self)

    def test_edit_movie_fail(self):
        test_edit_movie_fail(self)

    def test_delete_movie(self):
        test_delete_movie(self)

    def test_delete_movie_fail(self):
        test_delete_movie_fail(self)
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    app.run()