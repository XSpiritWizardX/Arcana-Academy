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
    bank_gold = db.Column(db.Integer, nullable=False, default=0)
    gems = db.Column(db.Integer, nullable=False, default=0)
    xp = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)

    # `turns` is the number of forest fights remaining in the current game day.
    turns = db.Column(db.Integer, nullable=False, default=10)
    specialty_uses = db.Column(db.Integer, nullable=False, default=5)
    game_day = db.Column(db.Integer, nullable=False, default=0)
    alive = db.Column(db.Boolean, nullable=False, default=True)

    weapon_level = db.Column(db.Integer, nullable=False, default=0)
    armor_level = db.Column(db.Integer, nullable=False, default=0)

    dragon_kills = db.Column(db.Integer, nullable=False, default=0)
    dragon_points = db.Column(db.Integer, nullable=False, default=0)
    dragon_attack = db.Column(db.Integer, nullable=False, default=0)
    dragon_defense = db.Column(db.Integer, nullable=False, default=0)
    dragon_hp = db.Column(db.Integer, nullable=False, default=0)
    dragon_fights = db.Column(db.Integer, nullable=False, default=0)

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
            "bank_gold": self.bank_gold,
            "gems": self.gems,
            "xp": self.xp,
            "level": self.level,
            "turns": self.turns,
            "specialty_uses": self.specialty_uses,
            "game_day": self.game_day,
            "alive": self.alive,
            "weapon_level": self.weapon_level,
            "armor_level": self.armor_level,
            "dragon_kills": self.dragon_kills,
            "dragon_points": self.dragon_points,
            "dragon_attack": self.dragon_attack,
            "dragon_defense": self.dragon_defense,
            "dragon_hp": self.dragon_hp,
            "dragon_fights": self.dragon_fights,
            "location": self.location,
        }
