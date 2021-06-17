import os
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    if test_config is not None and 'database_path' in test_config:
        setup_db(app, test_config['database_path'])
    else:
        setup_db(app)
    CORS(app)

    db = SQLAlchemy(app)

    @app.route('/', methods=['GET'])
    def get_index():
        return 'hello world'

    @app.route('/test', methods=['GET'])
    def get_test_page():
        return jsonify({
            'success': 'true'
        })

    @app.route('/movies', methods=['POST'])
    def add_movie():
        if request.get_json() is None:
            abort(400)
        # check the request actually specifies the data needed
        if not {'name'} <= set(request.get_json()):
            abort(400)
        name = request.get_json()['name']
        if not isinstance(name, str):
            abort(400)
        new_movie = Movie(name=name)
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({
            'success': 'true'
        })

    return app

if __name__ == '__main__':
    create_app()