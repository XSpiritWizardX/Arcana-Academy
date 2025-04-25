from app.models.db import db, environment, SCHEMA, add_prefix_for_prod

class Sword(db.Model):
    __tablename__ = 'swords'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    sword_gallery_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    damage = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    cost = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    mana_cost = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    element = db.Column(db.String(20), nullable=False)


    # Relationships
    # user = db.relationship("User", back_populates="player")
    # portfolio_stocks = db.relationship("Portfolio_Stock", back_populates="stock", cascade="all, delete-orphan")
    # watchlist_stocks = db.relationship("Watchlist_Stock", back_populates="stock", cascade="all, delete-orphan")
    # stock_transactions = db.relationship("Stock_Transaction", back_populates="stock", cascade="all, delete-orphan")



    def to_dict(self):
        return {
            'id': self.id,
            'sword_gallery_id': self.sword_gallery_id,
            'name': self.name,
            'description': self.description,
            'damage': self.damage,
            'cost': self.cost,
            'mana_cost': self.mana_cost,
            'element': self.element
        }
