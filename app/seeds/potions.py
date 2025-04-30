from app.models import db, Potion, environment, SCHEMA
from sqlalchemy.sql import text


def seed_potions():
    potion1 = Potion(
        user_id= 1, name='small potion', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",element='healing', cost=100, type="health", regeneration=670.80, description='A small healing potion.')

    potion2 = Potion(
        user_id= 1, name='medium potion', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",element='healing', cost=200, type="health", regeneration=1341.60, description='A medium healing potion.')
    potion3 = Potion(
        user_id= 1, name='large potion', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",element='healing', cost=300, type="health", regeneration=2012.40, description='A large healing potion.')
    potion4 = Potion(
        user_id= 1, name='small mana potion', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",element='mana', cost=100, type="mana", regeneration=670.80, description='A small mana potion.')
    potion5 = Potion(
        user_id= 1, name='medium mana potion', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",element='mana', cost=200, type="mana", regeneration=1341.60, description='A medium mana potion.')
    potion6 = Potion(
        user_id= 1, name='large mana potion', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",element='mana', cost=300, type="mana", regeneration=2012.40, description='A large mana potion.')

    db.session.add(potion1)
    db.session.add(potion2)
    db.session.add(potion3)
    db.session.add(potion4)
    db.session.add(potion5)
    db.session.add(potion6)

    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_potions():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.potions RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM potions"))

    db.session.commit()
