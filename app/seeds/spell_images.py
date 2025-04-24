from app.models import db, Spell_image, environment, SCHEMA
from sqlalchemy.sql import text


def seed_spell_images():
    # Add monster images here
    spell_image1 = Spell_image(
        spell_id=1,  url="https://images.unsplash.com/photo1",
    )
    spell_image2 = Spell_image(
        spell_id=2,  url="https://images.unsplash.com/photo2",
    )
    spell_image3 = Spell_image(
        spell_id=3,  url="https://images.unsplash.com/photo3",
    )
    spell_image4 = Spell_image(
        spell_id=4,  url="https://images.unsplash.com/photo4",
    )
    spell_image5 = Spell_image(
        spell_id=5,  url="https://images.unsplash.com/photo5",
    )
    spell_image6 = Spell_image(
        spell_id=6,  url="https://images.unsplash.com/photo6",
    )
    spell_image7 = Spell_image(
        spell_id=7,  url="https://images.unsplash.com/photo7",
    )
    spell_image8 = Spell_image(
        spell_id=8,  url="https://images.unsplash.com/photo8",
    )
    spell_image9 = Spell_image(
        spell_id=9,  url="https://images.unsplash.com/photo9",
    )
    spell_image10 = Spell_image(
        spell_id=10,  url="https://images.unsplash.com/photo10",
    )




    db.session.add(spell_image1)
    db.session.add(spell_image2)
    db.session.add(spell_image3)
    db.session.add(spell_image4)
    db.session.add(spell_image5)
    db.session.add(spell_image6)
    db.session.add(spell_image7)
    db.session.add(spell_image8)
    db.session.add(spell_image9)
    db.session.add(spell_image10)

    # Add other monster images here
    # Relationships




    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_spell_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.spell_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM spell_images"))

    db.session.commit()
