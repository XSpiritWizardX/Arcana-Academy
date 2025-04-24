from app.models.db import db, environment, SCHEMA, add_prefix_for_prod

class Monster_image(db.Model):
    __tablename__ = 'monster_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, nullable=False)
    # monster_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('monsters.id')), nullable=False)
    preview = db.Column(db.Boolean, nullable=False)
    url = db.Column(db.String(256), nullable=False)




    # Relationships
    # player = db.relationship("Player", back_populates="player")
    # monster = db.relationship("Monster", back_populates="monster_images")



    def to_dict(self):
        return {
            'id': self.id,
            'monster_id': self.monster_id,
            'preview': self.preview,
            'url': self.url
        }
