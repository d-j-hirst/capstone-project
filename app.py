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

  return app

APP = create_app()

@APP.route('/', methods=['GET'])
def drinks_short():
    return 'hello world'


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)