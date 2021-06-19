import os
from flask import Flask, request, abort, jsonify, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie

def error_400():
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400


def error_404():
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


def error_422():
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422


def error_500():
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

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

    @app.route('/movies/<int:movie_id>')
    def show_movie(movie_id):
        # shows the artist page with the given artist_id
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie is None:
            abort(404)
        movie_data = {
            'id': movie.id,
            'name': movie.name,
            'release_date': movie.release_date
        }
        return jsonify({
            'success': True,
            'movie_data': movie_data
        })

    @app.route('/movies/search', methods=['POST'])
    def search_movies():
        if request.get_json() is None:
            abort(400)
        if not {'search_term'} <= set(request.get_json()):
            abort(400)
        search_term = request.get_json()['search_term']
        # Case-insenstive search with any characters before or after the search term
        movies = Movie.query.filter(Movie.name.ilike('%' + search_term + '%')).all()
        movie_data = {
            'count': len(movies),
            'data': []
        }
        for movie in movies:
          movie_data['data'].append({
              "id": movie.id,
              "name": movie.name,
              "release_date": movie.release_date,
          })
        return jsonify({
            'success': True,
            'movie_data': movie_data
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def edit_movie(movie_id):
        if request.get_json() is None:
            abort(400)
        # check the request actually specifies the data needed
        if not {'name'} <= set(request.get_json()):
            abort(400)
        movie = Movie.query.filter_by(id=movie_id).first()
        name = request.get_json()['name']
        if not isinstance(name, str):
            abort(400)
        # Check there is a movie with requested id
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie is None:
            abort(404)
        db.session.query(Movie).\
            filter(Movie.id == movie_id).\
            update({'name': name})
        db.session.commit()
        return jsonify({
            'success': True
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
            'success': True
        })

    @app.errorhandler(400)
    def not_found(error):
        return error_400()

    @app.errorhandler(404)
    def not_found(error):
        return error_404()

    @app.errorhandler(422)
    def not_found(error):
        return error_422()

    @app.errorhandler(500)
    def not_found(error):
        return error_500()
    return app

if __name__ == '__main__':
    create_app()