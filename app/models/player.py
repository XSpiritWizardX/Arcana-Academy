from .db import db, environment, SCHEMA, add_prefix_for_prod

class Player(db.Model):
    __tablename__ = 'players'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    magic_class = db.Column(db.String(20), nullable=False)
    element = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    xp = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    gold = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    health = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    mana = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    damage = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    speed = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    strength = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    intellect = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    dexterity = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    vitality = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="player")
    # portfolio_stocks = db.relationship("Portfolio_Stock", back_populates="stock", cascade="all, delete-orphan")
    # watchlist_stocks = db.relationship("Watchlist_Stock", back_populates="stock", cascade="all, delete-orphan")
    # stock_transactions = db.relationship("Stock_Transaction", back_populates="stock", cascade="all, delete-orphan")



    def to_dict(self):
        return {
            'id': self.id,
            "user_id": self.user_id,
            'name': self.name,
            "url": self.url,
            'magic_class': self.magic_class,
            'element': self.element,
            'level': self.level,
            'xp': self.xp,
            'gold': self.gold,
            'health': self.health,
            'mana': self.mana,
            'damage': self.damage,
            'speed': self.speed,
            'strength': self.strength,
            'intellect': self.intellect,
            'dexterity': self.dexterity,
            'vitality': self.vitality
        }
