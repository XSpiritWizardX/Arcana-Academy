from app.models.db import db, environment, SCHEMA, add_prefix_for_prod

class Spell_image(db.Model):
    __tablename__ = 'spell_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(256), nullable=False)




    # Relationships
    # player = db.relationship("Player", back_populates="player")
    # monster = db.relationship("Monster", back_populates="monster_images")



    def to_dict(self):
        return {
            'id': self.id,
            'spell_id': self.spell_id,
            'url': self.url
        }
