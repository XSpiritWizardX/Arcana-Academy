from app.models.db import db, environment, SCHEMA, add_prefix_for_prod

class Potion(db.Model):
    __tablename__ = 'potions'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    regeneration = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    cost = db.Column(db.Numeric(precision=20, scale=2, asdecimal=True), nullable=False)
    element = db.Column(db.String(20), nullable=False)


    # Relationships
    user = db.relationship("User", back_populates="potion")
    # portfolio_stocks = db.relationship("Portfolio_Stock", back_populates="stock", cascade="all, delete-orphan")
    # watchlist_stocks = db.relationship("Watchlist_Stock", back_populates="stock", cascade="all, delete-orphan")
    # stock_transactions = db.relationship("Stock_Transaction", back_populates="stock", cascade="all, delete-orphan")



    def to_dict(self):
        return {
            'id': self.id,
            "user_id": self.user_id,
            "url": self.url,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'regeneration': self.regeneration,
            'cost': self.cost,
            'element': self.element
        }
