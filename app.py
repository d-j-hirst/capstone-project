import os
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def get_index():
        return 'hello world'

    @app.route('/test', methods=['GET'])
    def get_test_page():
        return jsonify({
            'success': 'true'
        })

    return app

if __name__ == '__main__':
    create_app()