from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    # Relationships
    player = db.relationship("Player", back_populates="user", cascade="all, delete-orphan")
    spell = db.relationship("Spell", back_populates="user", cascade="all, delete-orphan", uselist=False)
    potion = db.relationship("Potion", back_populates="user", cascade="all, delete-orphan", uselist=False)
    sword = db.relationship("Sword", back_populates="user", cascade="all, delete-orphan", uselist=False)
    schedule = db.relationship("Schedule", back_populates="user", cascade="all, delete-orphan", uselist=False)
    review = db.relationship("Review", back_populates="user", cascade="all, delete-orphan", uselist=False)




    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
