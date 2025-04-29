from app.models import db, Sword, environment, SCHEMA
from sqlalchemy.sql import text


def seed_swords():
    sword1 = Sword(
        sword_gallery_id=1, name='Volcano', element='Fire', cost=100, mana_cost=30, damage=670.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Unleash a fiery eruption that engulfs the battlefield, dealing massive damage to all enemies in range.')
    sword2 = Sword(
        sword_gallery_id=2, name='Frost Nova', element='Ice', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Freeze your enemies in place with a blast of icy wind, dealing damage and immobilizing them for a short duration.')
    sword3 = Sword(
        sword_gallery_id=3, name='Lightning Bolt', element='Lightning', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Call down a bolt of lightning to strike your enemies, dealing massive damage and stunning them for a short duration.')
    sword4 = Sword(
        sword_gallery_id=4, name='Earthquake', element='Earth', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Create a massive earthquake that shakes the ground and deals damage to all enemies in range.')
    sword5 = Sword(
        sword_gallery_id=5, name='Thunderstorm', element='Lightning', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Summon a powerful thunderstorm that strikes your enemies with lightning, dealing massive damage and stunning them for a short duration.')
    sword6 = Sword(
        sword_gallery_id=6, name='Shadow Bolt', element='Shadow', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Launch a bolt of dark energy at your enemies, dealing damage and reducing their defenses for a short duration.')
    sword7 = Sword(
        sword_gallery_id=7, name='Holy Light', element='Light', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Heal your allies with a burst of holy energy, restoring their health and removing negative effects.')
    sword8 = Sword(
        sword_gallery_id=1, name='Water Surge', element='Water', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Unleash a powerful surge of water that deals damage to all enemies in range and heals your allies.')
    sword9 = Sword(
        sword_gallery_id=2, name='Wind Blade', element='Wind', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Slice through your enemies with a blade of wind, dealing damage and knocking them back.')
    sword10 = Sword(
        sword_gallery_id=3, name='Earth Shield', element='Earth', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Create a protective shield of earth around your allies, reducing damage taken and increasing their defenses.')
    sword11 = Sword(
        sword_gallery_id=4, name='Fireball', element='Fire', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Launch a fiery ball of energy at your enemies, dealing damage and igniting them for additional damage over time.')
    sword12 = Sword(
        sword_gallery_id=5, name='Ice Spike', element='Ice', cost=100, mana_cost=30, damage=6070.80, url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg", description='Launch a spike of ice at your enemies, dealing damage and slowing their movement speed.')


    db.session.add(sword1)
    db.session.add(sword2)
    db.session.add(sword3)
    db.session.add(sword4)
    db.session.add(sword5)
    db.session.add(sword6)
    db.session.add(sword7)
    db.session.add(sword8)
    db.session.add(sword9)
    db.session.add(sword10)
    db.session.add(sword11)
    db.session.add(sword12)

    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_swords():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.swords RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM swords"))

    db.session.commit()
