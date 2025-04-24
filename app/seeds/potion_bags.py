from app.models import db, Potion_bag, environment, SCHEMA
from sqlalchemy.sql import text


def seed_potion_bags():
    potion_bag1 = Potion_bag(
        user_id=3, name='Healing Bag', magic_class="Health")
    potion_bag2 = Potion_bag(
        user_id=4, name='Mana Bag', magic_class="Mana")
    potion_bag3 = Potion_bag(
        user_id=1, name='Stamina Bag', magic_class="Stamina")
    potion_bag4 = Potion_bag(
        user_id=2, name='Strength Bag', magic_class="Strength")
    potion_bag5 = Potion_bag(
        user_id=5, name='Agility Bag', magic_class="Agility")
    potion_bag6 = Potion_bag(
        user_id=1, name='Intelligence Bag', magic_class="Intelligence")
    potion_bag7 = Potion_bag(
        user_id=2, name='Wisdom Bag', magic_class="Wisdom")
    potion_bag8 = Potion_bag(
        user_id=3, name='Charisma Bag', magic_class="Charisma")
    potion_bag9 = Potion_bag(
        user_id=4, name='Dexterity Bag', magic_class="Dexterity")
    potion_bag10 = Potion_bag(
        user_id=5, name='Endurance Bag', magic_class="Endurance")
    potion_bag11 = Potion_bag(
        user_id=1, name='Luck Bag', magic_class="Luck")

    db.session.add(potion_bag1)
    db.session.add(potion_bag2)
    db.session.add(potion_bag3)
    db.session.add(potion_bag4)
    db.session.add(potion_bag5)
    db.session.add(potion_bag6)
    db.session.add(potion_bag7)
    db.session.add(potion_bag8)
    db.session.add(potion_bag9)
    db.session.add(potion_bag10)
    db.session.add(potion_bag11)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_potion_bags():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.potion_bags RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM potion_bags"))

    db.session.commit()
