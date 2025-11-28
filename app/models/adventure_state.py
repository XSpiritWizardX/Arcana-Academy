from .db import db, environment, SCHEMA, add_prefix_for_prod


class AdventureState(db.Model):
    __tablename__ = "adventure_states"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False, unique=True
    )
    hp = db.Column(db.Integer, nullable=False, default=20)
    max_hp = db.Column(db.Integer, nullable=False, default=20)
    attack = db.Column(db.Integer, nullable=False, default=5)
    defense = db.Column(db.Integer, nullable=False, default=2)
    gold = db.Column(db.Integer, nullable=False, default=0)
    xp = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)
    turns = db.Column(db.Integer, nullable=False, default=10)
    dragon_kills = db.Column(db.Integer, nullable=False, default=0)
    location = db.Column(db.String(50), nullable=False, default="town")

    user = db.relationship("User", back_populates="adventure_state")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "gold": self.gold,
            "xp": self.xp,
            "level": self.level,
            "turns": self.turns,
            "dragon_kills": self.dragon_kills,
            "location": self.location,
        }
