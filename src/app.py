"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'birth_year': p.birth_year} for p in people])


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get_or_404(people_id)
    return jsonify({'id': person.id, 'name': person.name, 'birth_year': person.birth_year})


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'climate': p.climate} for p in planets])


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify({'id': planet.id, 'name': planet.name, 'climate': planet.climate})


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    favorite_characters = FavoriteCharacter.query.filter_by(
        user_id=user_id).all()
    favorite_planets = FavoritePlanet.query.filter_by(user_id=user_id).all()
    response = {
        'favorite_characters': [f.to_dict() for f in favorite_characters],
        'favorite_planets': [f.to_dict() for f in favorite_planets]
    }
    return jsonify(response)


@app.route('/register', methods=['POST'])
def register_user():
    body = request.get_json()
    email = body['email']
    username = body['username']
    password = body['password']
    if body is None:
        raise APIException(
            'You need to specify the request body as json object', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'username' not in body:
        raise APIException('You need to specify the username', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    new_user = User(email=email, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added"}), 201


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
