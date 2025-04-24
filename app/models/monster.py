from .db import db, environment, SCHEMA, add_prefix_for_prod

class Monster(db.Model):
    __tablename__ = 'monsters'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    element = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    health = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    gold_drop = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)



    # Relationships
    # player = db.relationship("Player", back_populates="player")



    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'element': self.element,
            'description': self.description,
            'health': self.health,
            'gold_drop': self.gold_drop
        }
