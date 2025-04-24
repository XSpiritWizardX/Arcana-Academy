from app.models import db, Sword_gallery, environment, SCHEMA
from sqlalchemy.sql import text


def seed_sword_galleries():
    sword_gallery1 = Sword_gallery(
        user_id=3, name='ancient swords', magic_class="Ancient Magic")
    sword_gallery2 = Sword_gallery(
        user_id=3, name='sword of the ancients', magic_class="Ancient Magic")
    sword_gallery3 = Sword_gallery(
        user_id=3, name='ice swords', magic_class="Ice Magic")
    sword_gallery4 = Sword_gallery(
        user_id=3, name='fire swords', magic_class="Fire Magic")
    sword_gallery5 = Sword_gallery(
        user_id=3, name='lightning swords', magic_class="Lightning Magic")
    sword_gallery6 = Sword_gallery(
        user_id=3, name='shadow swords', magic_class="Shadow Magic")
    sword_gallery7 = Sword_gallery(
        user_id=3, name='light swords', magic_class="Light Magic")

    db.session.add(sword_gallery1)
    db.session.add(sword_gallery2)
    db.session.add(sword_gallery3)
    db.session.add(sword_gallery4)
    db.session.add(sword_gallery5)
    db.session.add(sword_gallery6)
    db.session.add(sword_gallery7)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_sword_galleries():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.sword_galleries RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM sword_galleries"))

    db.session.commit()
