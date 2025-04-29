from app.models import db, Stage, environment, SCHEMA
from sqlalchemy.sql import text


def seed_stages():
    stage1 = Stage(
        monster_id=1, player_id=1, background_id=1, element='TIME', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",description="This wizard has been known for many ages now. from the time a sword was in a stone ")
    stage2 = Stage(
        monster_id=2, player_id=1, background_id=2, element='LIGHTNING', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",description="This wizard has been known for many ages now. from the time a sword was in a stone ")
    stage3 = Stage(
        monster_id=3, player_id=1, background_id=3, element='FIRE', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",description="This wizard has been known for many ages now. from the time a sword was in a stone ")
    stage4 = Stage(
        monster_id=4, player_id=1, background_id=4, element='EARTH', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",description="This wizard has been known for many ages now. from the time a sword was in a stone ")
    stage5 = Stage(
        monster_id=5, player_id=1, background_id=5, element='WIND', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",description="This wizard has been known for many ages now. from the time a sword was in a stone ")
    stage6 = Stage(
        monster_id=6, player_id=1, background_id=6, element='WATER', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",description="This wizard has been known for many ages now. from the time a sword was in a stone ")
    stage7 = Stage(
        monster_id=7, player_id=1, background_id=7, element='EARTH', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",description="This wizard has been known for many ages now. from the time a sword was in a stone ")

    db.session.add(stage1)
    db.session.add(stage2)
    db.session.add(stage3)
    db.session.add(stage4)
    db.session.add(stage5)
    db.session.add(stage6)
    db.session.add(stage7)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_stages():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.stages RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM stages"))

    db.session.commit()
