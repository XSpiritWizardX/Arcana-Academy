from .db import db, environment, SCHEMA, add_prefix_for_prod

class Schedule(db.Model):
    __tablename__ = 'schedules'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)



    # Relationships
    # player = db.relationship("Player", back_populates="player")
    # monster_images = db.relationship("Monster_image", back_populates="monster", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'description': self.description
        }
