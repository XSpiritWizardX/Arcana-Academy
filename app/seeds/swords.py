from app.models import db, Sword, environment, SCHEMA
from sqlalchemy.sql import text


def seed_swords():
    sword1 = Sword(
        user_id= 1, name='Flameberg', element='Fire', cost=100, mana_cost=30, damage=670.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Unleash a fiery eruption that engulfs the battlefield, dealing massive damage to all enemies in range.')
    sword2 = Sword(
        user_id= 1, name='Blue Rose', element='Ice', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Freeze your enemies in place with a blast of icy wind, dealing damage and immobilizing them for a short duration.')
    sword3 = Sword(
        user_id= 1, name='Lightnyan Rod', element='Lightning', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Call down a bolt of lightning to strike your enemies, dealing massive damage and stunning them for a short duration.')
    sword4 = Sword(
        user_id= 1, name='Mud Sword', element='Earth', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Create a massive earthquake that shakes the ground and deals damage to all enemies in range.')
    sword5 = Sword(
        user_id= 1, name='Master Sword', element='Light', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1746579226/master_sword_fvni1l.gif", description='Summon a powerful thunderstorm that strikes your enemies with lightning, dealing massive damage and stunning them for a short duration.')
    sword6 = Sword(
        user_id= 1, name='Ceremonial Daggers', element='Shadow', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Launch a bolt of dark energy at your enemies, dealing damage and reducing their defenses for a short duration.')
    sword7 = Sword(
        user_id= 2, name='Excalibur', element='Light', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Heal your allies with a burst of holy energy, restoring their health and removing negative effects.')
    sword8 = Sword(
        user_id= 2, name='Water Pick', element='Water', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Unleash a powerful surge of water that deals damage to all enemies in range and heals your allies.')
    sword9 = Sword(
        user_id= 2, name='Wind Blade', element='Wind', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Slice through your enemies with a blade of wind, dealing damage and knocking them back.')
    sword10 = Sword(
        user_id= 2, name='Cutlass', element='Earth', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Create a protective shield of earth around your allies, reducing damage taken and increasing their defenses.')
    sword11 = Sword(
        user_id= 2, name='Fire Katana', element='Fire', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Launch a fiery ball of energy at your enemies, dealing damage and igniting them for additional damage over time.')
    sword12 = Sword(
        user_id= 2, name='Ice Katana', element='Ice', cost=100, mana_cost=30, damage=6070.80, url = "https://res.cloudinary.com/dl6ls3rgu/image/upload/v1745485217/c4VelOqJ0XGgVN4m3ALp--0--sdzke_bg-rmvd_kc3dfy.png", description='Launch a spike of ice at your enemies, dealing damage and slowing their movement speed.')


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
