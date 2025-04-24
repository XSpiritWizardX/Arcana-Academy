from app.models import db, Spell, environment, SCHEMA
from sqlalchemy.sql import text


def seed_spells():
    spell1 = Spell(
        spell_book_id=1, name='Volcano', element='Fire', cost=100, mana_cost=30, damage=670.80, description='Unleash a fiery eruption that engulfs the battlefield, dealing massive damage to all enemies in range.')
    spell2 = Spell(
        spell_book_id=2, name='Frost Nova', element='Ice', cost=100, mana_cost=30, damage=6070.80, description='Freeze your enemies in place with a blast of icy wind, dealing damage and immobilizing them for a short duration.')
    spell3 = Spell(
        spell_book_id=3, name='Lightning Bolt', element='Lightning', cost=100, mana_cost=30, damage=6070.80, description='Call down a bolt of lightning to strike your enemies, dealing massive damage and stunning them for a short duration.')
    spell4 = Spell(
        spell_book_id=4, name='Earthquake', element='Earth', cost=100, mana_cost=30, damage=6070.80, description='Create a massive earthquake that shakes the ground and deals damage to all enemies in range.')
    spell5 = Spell(
        spell_book_id=5, name='Thunderstorm', element='Lightning', cost=100, mana_cost=30, damage=6070.80, description='Summon a powerful thunderstorm that strikes your enemies with lightning, dealing massive damage and stunning them for a short duration.')
    spell6 = Spell(
        spell_book_id=6, name='Shadow Bolt', element='Shadow', cost=100, mana_cost=30, damage=6070.80, description='Launch a bolt of dark energy at your enemies, dealing damage and reducing their defenses for a short duration.')
    spell7 = Spell(
        spell_book_id=7, name='Holy Light', element='Light', cost=100, mana_cost=30, damage=6070.80, description='Heal your allies with a burst of holy energy, restoring their health and removing negative effects.')
    spell8 = Spell(
        spell_book_id=1, name='Water Surge', element='Water', cost=100, mana_cost=30, damage=6070.80, description='Unleash a powerful surge of water that deals damage to all enemies in range and heals your allies.')
    spell9 = Spell(
        spell_book_id=2, name='Wind Blade', element='Wind', cost=100, mana_cost=30, damage=6070.80, description='Slice through your enemies with a blade of wind, dealing damage and knocking them back.')
    spell10 = Spell(
        spell_book_id=3, name='Earth Shield', element='Earth', cost=100, mana_cost=30, damage=6070.80, description='Create a protective shield of earth around your allies, reducing damage taken and increasing their defenses.')
    spell11 = Spell(
        spell_book_id=4, name='Fireball', element='Fire', cost=100, mana_cost=30, damage=6070.80, description='Launch a fiery ball of energy at your enemies, dealing damage and igniting them for additional damage over time.')
    spell12 = Spell(
        spell_book_id=5, name='Ice Spike', element='Ice', cost=100, mana_cost=30, damage=6070.80, description='Launch a spike of ice at your enemies, dealing damage and slowing their movement speed.')
    spell13 = Spell(
        spell_book_id=6, name='Shadow Step', element='Shadow', cost=100, mana_cost=30, damage=6070.80, description='Teleport behind your enemies and deal damage, stunning them for a short duration.')
    spell14 = Spell(
        spell_book_id=7, name='Light Beam', element='Light', cost=100, mana_cost=30, damage=6070.80, description='Unleash a beam of holy light that deals damage to your enemies and heals your allies.')
    spell15 = Spell(
        spell_book_id=8, name='Water Shield', element='Water', cost=100, mana_cost=30, damage=6070.80, description='Create a protective shield of water around your allies, reducing damage taken and increasing their mana regeneration.')



    db.session.add(spell1)
    db.session.add(spell2)
    db.session.add(spell3)
    db.session.add(spell4)
    db.session.add(spell5)
    db.session.add(spell6)
    db.session.add(spell7)
    db.session.add(spell8)
    db.session.add(spell9)
    db.session.add(spell10)
    db.session.add(spell11)
    db.session.add(spell12)
    db.session.add(spell13)
    db.session.add(spell14)
    db.session.add(spell15)

    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_spells():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.spells RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM spells"))

    db.session.commit()
