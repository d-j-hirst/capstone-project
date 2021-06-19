from models import Movie
from flask import abort, jsonify, request

def setup_movie_routes(app, db):
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