import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from config import AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE

database_name = "nomadic"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_creat_all():
    db.drop_all()
    db.create_all()
    db_init_records()


def db_init_records():
    client = Client(
        name='Fyyur',
        description='Platform that connects musicians and venues'
    )
    artist = Artist(
        name='Picasso',
        portfolio_link='https://www.behance.net'
    )
    project = Project(
        name='Fyyur website background',
        client_id=1,
        description='Digital background art for the Fyyer website'
    )
    client.insert()
    artist.insert()
    project.insert()


'''
Artist
'''


class Artist(db.Model):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    portfolio_link = Column(String, nullable=False)

    def __init__(self, name, portfolio_link):
        self.name = name
        self.portfolio_link = portfolio_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'portfolio_link': self.portfolio_link
        }


'''
Client
'''


class Client(db.Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


'''
Project
'''


class Project(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    client_id = Column(Integer, db.ForeignKey('client.id'), primary_key=True)
    is_open = Column(db.Boolean, nullable=False, default=True)
    description = Column(String, nullable=False)

    def __init__(self, name, client_id, description):
        self.name = name
        self.client_id = client_id
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'client_id': self.client_id,
            'isOpen': self.is_open,
            'description': self.description
        }

