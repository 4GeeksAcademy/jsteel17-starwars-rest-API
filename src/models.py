from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    favorite_character = db.relationship('FavoriteCharacter', backref = 'user', lazy=True)
    favorite_planet = db.relationship('FavoritePlanet', backref = 'user', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    birth_year = db.Column(String(20), nullable=True)
    gender = db.Column(String(20), nullable=True)
    height = db.Column(String(10), nullable=True)
    mass = db.Column(String(10), nullable=True)
    hair_color = db.Column(String(50), nullable=True)
    skin_color = db.Column(String(50), nullable=True)
    eye_color = db.Column(String(50), nullable=True)

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color
        }

class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    climate = db.Column(String(100), nullable=True)
    terrain = db.Column(String(100), nullable=True)
    population = db.Column(String(50), nullable=True)
    gravity = db.Column(String(50), nullable=True)
    diameter = db.Column(String(50), nullable=True)


    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "gravity": self.gravity,
            "diameter": self.diameter
        }

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": User.query.get(self.user_id).serialize(),
            "planet": Planet.query.get(self.planet_id).serialize()
        }


class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user": User.query.get(self.user_id).serialize(),
            "character": Character.query.get(self.character_id).serialize()
        }



