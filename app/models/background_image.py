from .db import db, environment, SCHEMA, add_prefix_for_prod

class Background_image(db.Model):
    __tablename__ = 'background_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), nullable=False)




    # Relationships
    # player = db.relationship("Player", back_populates="player")



    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url
        }
