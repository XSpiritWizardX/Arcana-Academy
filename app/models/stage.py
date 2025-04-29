from .db import db, environment, SCHEMA, add_prefix_for_prod

class Stage(db.Model):
    __tablename__ = 'stages'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, nullable=False)
    # monster_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('monsters.id')), nullable=False)
    player_id = db.Column(db.Integer, nullable=False)
    background_id = db.Column(db.Integer, nullable=False)
    element = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)




    # Relationships
    # player = db.relationship("Player", back_populates="player")



    def to_dict(self):
        return {
            'id': self.id,
            'monster_id': self.monster_id,
            'player_id': self.player_id,
            'background_id': self.background_id,
            'element': self.element,
            'description': self.description,
            "url": self.url
        }
