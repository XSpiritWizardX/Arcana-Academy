from app.models import db, Player, environment, SCHEMA
from sqlalchemy.sql import text


def seed_players():
    player1 = Player(
        user_id=1, name='MERLIN', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Wizard', element='TIME', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player2 = Player(
        user_id=1, name='GANDALF', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Wizard', element='LIGHTNING', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player3 = Player(
        user_id=1, name='HARRY', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Wizard', element='FIRE', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player4 = Player(
        user_id=1, name='FRODO', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Rogue', element='EARTH', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player5 = Player(
        user_id=1, name='ARAGORN', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Rogue', element='WIND', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player6 = Player(
        user_id=1, name='LEGOLAS', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Rogue', element='WATER', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player7 = Player(
        user_id=1, name='THORIN', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Warrior', element='EARTH', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player8 = Player(
        user_id=1, name='GIMLI', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Warrior', element='FIRE', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player9 = Player(
        user_id=1, name='THOR', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Warrior', element='LIGHTNING', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)
    player10 = Player(
        user_id=1, name='LUCY', url = "https://img.freepik.com/premium-psd/monster-cartoon-character-design-illustration-transparent-background_187482-2075.jpg",magic_class='Paladin', element='WATER', level=1, xp=0, gold=100, health=100, mana=50, damage=10, speed=5, strength=10, intellect=5, dexterity=5, vitality=10)


    db.session.add(player1)
    db.session.add(player2)
    db.session.add(player3)
    db.session.add(player4)
    db.session.add(player5)
    db.session.add(player6)
    db.session.add(player7)
    db.session.add(player8)
    db.session.add(player9)
    db.session.add(player10)


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_players():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.players RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM players"))

    db.session.commit()
