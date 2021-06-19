from models import Actor
from flask import abort, jsonify, request

def setup_actor_routes(app, db):
    @app.route('/actors/<int:actor_id>')
    def show_actor(actor_id):
        # shows the artist page with the given artist_id
        actor = Actor.query.filter_by(id=actor_id).first()
        if actor is None:
            abort(404)
        actor_data = {
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender
        }
        return jsonify({
            'success': True,
            'actor_data': actor_data
        })

    @app.route('/actors/search', methods=['POST'])
    def search_actors():
        if request.get_json() is None:
            abort(400)
        if not {'search_term'} <= set(request.get_json()):
            abort(400)
        search_term = request.get_json()['search_term']
        # Case-insenstive search with any characters before or after the search term
        actors = Actor.query.filter(Actor.name.ilike('%' + search_term + '%')).all()
        actor_data = {
            'count': len(actors),
            'data': []
        }
        for actor in actors:
            actor_data['data'].append({
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            })
        return jsonify({
            'success': True,
            'actor_data': actor_data
        })

    @app.route('/actors', methods=['POST'])
    def add_actor():
        if request.get_json() is None:
            abort(400)
        # check the request actually specifies the data needed
        if not {'name', 'age', 'gender'} <= set(request.get_json()):
            abort(400)
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']
        if not isinstance(name, str) or not isinstance(age, int) or \
                not isinstance(gender, str):
            abort(400)
        new_actor = Actor(name=name, age=age, gender=gender)
        db.session.add(new_actor)
        db.session.commit()
        return jsonify({
            'success': True
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def edit_actor(actor_id):
        if request.get_json() is None:
            abort(400)
        # check the request actually specifies the data needed
        if not {'name', 'age', 'gender'} <= set(request.get_json()):
            abort(400)
        name = request.get_json()['name']
        age = request.get_json()['age']
        gender = request.get_json()['gender']
        if not isinstance(name, str) or not isinstance(age, int) or \
                not isinstance(gender, str):
            abort(400)
        # Check there is a actor with requested id
        actor = Actor.query.filter_by(id=actor_id).first()
        if actor is None:
            abort(404)
        db.session.query(Actor).\
            filter(Actor.id == actor_id).\
            update({'name': name, 'age': age, 'gender': gender})
        db.session.commit()
        return jsonify({
            'success': True
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        # Check there is a actor with requested id
        actor = Actor.query.filter_by(id=actor_id).first()
        if actor is None:
            abort(404)
        db.session.query(Actor).\
            filter(Actor.id == actor_id).delete()
        db.session.commit()
        return jsonify({
            'success': True
        })