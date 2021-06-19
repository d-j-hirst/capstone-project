import os
from flask import Flask, request, abort, jsonify, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie

from routes_movies import *
from error_handling import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    if test_config is not None and 'database_path' in test_config:
        setup_db(app, test_config['database_path'])
    else:
        setup_db(app)
    CORS(app)

    db = SQLAlchemy(app)

    #setup routes
    setup_movie_routes(app, db)
    setup_error_handlers(app)

    return app

if __name__ == '__main__':
    create_app()