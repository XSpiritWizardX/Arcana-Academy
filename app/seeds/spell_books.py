from app.models import db, Spell_book, environment, SCHEMA
from sqlalchemy.sql import text


def seed_spell_books():
    spellbook1 = Spell_book(
        user_id=3, name='eruption magic', magic_class="Fire Mage")
    spellbook2 = Spell_book(
        user_id=4, name='frost magic', magic_class="Ice Mage")
    spellbook3 = Spell_book(
        user_id=1, name='storm magic', magic_class="Storm Mage")
    spellbook4 = Spell_book(
        user_id=2, name='earth magic', magic_class="Earth Mage")
    spellbook5 = Spell_book(
        user_id=5, name='lightning magic', magic_class="Lightning Mage")
    spellbook6 = Spell_book(
        user_id=1, name='shadow magic', magic_class="Shadow Mage")
    spellbook7 = Spell_book(
        user_id=2, name='light magic', magic_class="Light Mage")
    spellbook8 = Spell_book(
        user_id=3, name='water magic', magic_class="Water Mage")
    spellbook9 = Spell_book(
        user_id=4, name='wind magic', magic_class="Wind Mage")
    spellbook10 = Spell_book(
        user_id=5, name='earth magic', magic_class="Earth Mage")

    db.session.add(spellbook1)
    db.session.add(spellbook2)
    db.session.add(spellbook3)
    db.session.add(spellbook4)
    db.session.add(spellbook5)
    db.session.add(spellbook6)
    db.session.add(spellbook7)
    db.session.add(spellbook8)
    db.session.add(spellbook9)
    db.session.add(spellbook10)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_spell_books():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.spell_books RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM spell_books"))

    db.session.commit()
