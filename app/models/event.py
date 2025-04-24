
from .db import db, environment, SCHEMA, add_prefix_for_prod

class Event(db.Model):
    __tablename__ = 'events'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    time = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)



    # Relationships
    # player = db.relationship("Player", back_populates="player")
    # monster_images = db.relationship("Monster_image", back_populates="monster", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'date': self.date,
            'description': self.description
        }
