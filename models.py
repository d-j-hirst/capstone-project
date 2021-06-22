from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

# Get the database path from an environment variable
# Heroku automatically generates a DATABASE_URL beginning with
#  "postgres://" (which can't be easily edited), while SQLAlchemy in
#  its latest version will only work with "postgresql://". This
#  adjustment allows compatibility between the two by converting
#  the scheme of Heroku's URL
database_path = os.environ.get('DATABASE_URL').replace("s://", "sql://", 1)

db = SQLAlchemy()


# setup_db(app)
# binds a flask application and a SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    release_date = Column(DateTime)


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
