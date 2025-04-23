from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_users():
    demo = User(
       firstname='Demo', lastname='User', username='Demo', email='demo@aa.io', password='password', gold=0, experience=0, level=1, health=100, speed=10, power=10, mana=10)
    marnie = User(
        firstname='MAR', lastname='MARNI', username='marnie', email='marnie@aa.io', password='password', gold=0, experience=0, level=1, health=100, speed=10, power=10, mana=10)
    bobbie = User(
        firstname='BOB', lastname='BOBBIE', username='bobbie', email='bobbie@aa.io', password='password', gold=0, experience=0, level=1, health=100, speed=10, power=10, mana=10)
    legolas = User(
        firstname='Legolas', lastname='LOTR', username='Archer', email='lego@aa.io', password='password', gold=0, experience=0, level=1, health=100, speed=10, power=10, mana=10)
    frodo = User(
        firstname='Frodo', lastname='Baggins', username='ringbearer', email='baggins@aa.io', password='password', gold=0, experience=0, level=1, health=100, speed=10, power=10, mana=10)
    gandalf = User(
        firstname='Gandalf', lastname='The Grey', username='Wizard', email='wizard@aa.io', password='password', gold=0, experience=0, level=1, health=100, speed=10, power=10, mana=10)

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.add(legolas)
    db.session.add(frodo)
    db.session.add(gandalf)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
