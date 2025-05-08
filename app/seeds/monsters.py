from app.models import db, Monster, environment, SCHEMA
from sqlalchemy.sql import text


def seed_monsters():
    monster1 = Monster(
        name="GREEN DRAGON", element='TIME', description="This Monster has been on the loose for the longest time now.", url="none",health=100000.00, gold_drop=320000.99)
    monster2 = Monster(
        name="RED DRAGON", element='LIGHTNING', description="This Monster has been on the loose for the longest time now.", url="none",health=.00, gold_drop=320000.99)
    monster3 = Monster(
        name="BLUE DRAGON", element='FIRE', description="This Monster has been on the loose for the longest time now.", url="none", health=.00, gold_drop=320000.99)
    monster4 = Monster(
        name="BLACK DRAGON", element='EARTH', description="This Monster has been on the loose for the longest time now.", url="htnone",health=.00, gold_drop=320000.99)
    monster5 = Monster(
        name="WHITE DRAGON", element='WIND', description="This Monster has been on the loose for the longest time now.", url="htnone",health=.00, gold_drop=320000.99)
    monster6 = Monster(
        name="YELLOW DRAGON", element='WATER', description="This Monster has been on the loose for the longest time now.", url="htnone",health=.00, gold_drop=320000.99)
    monster7 = Monster(
        name="BROWN DRAGON", element='EARTH', description="This Monster has been on the loose for the longest time now.", url="htnone",health=.00, gold_drop=320000.99)
    monster8 = Monster(
        name="PURPLE DRAGON", element='FIRE', description="This Monster has been on the loose for the longest time now.", url="htnone",health=.00, gold_drop=320000.99)
    monster9 = Monster(
        name="PINK DRAGON", element='LIGHTNING', description="This Monster has been on the loose for the longest time now.", url="htnone",health=.00, gold_drop=320000.99)
    monster10 = Monster(
        name="ORANGE DRAGON", element='WATER', description="This Monster has been on the loose for the longest time now.", url="htnone",health=.00, gold_drop=320000.99)

    db.session.add(monster1)
    db.session.add(monster2)
    db.session.add(monster3)
    db.session.add(monster4)
    db.session.add(monster5)
    db.session.add(monster6)
    db.session.add(monster7)
    db.session.add(monster8)
    db.session.add(monster9)
    db.session.add(monster10)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_monsters():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.monsters RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM monsters"))

    db.session.commit()
