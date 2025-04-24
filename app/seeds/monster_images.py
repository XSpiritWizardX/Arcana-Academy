from app.models import db, Monster_image, environment, SCHEMA
from sqlalchemy.sql import text


def seed_monster_images():
    # Add monster images here
    monster_image1 = Monster_image(
        monster_id=1, preview=True, url="https://images.unsplash.com/photo1",
    )
    monster_image2 = Monster_image(
        monster_id=1, preview=False, url="https://images.unsplash.com/photo2",
    )
    monster_image3 = Monster_image(
        monster_id=2, preview=True, url="https://images.unsplash.com/photo3",
    )
    monster_image4 = Monster_image(
        monster_id=2, preview=False, url="https://images.unsplash.com/photo4",
    )
    monster_image5 = Monster_image(
        monster_id=3, preview=True, url="https://images.unsplash.com/photo5",
    )
    monster_image6 = Monster_image(
        monster_id=3, preview=False, url="https://images.unsplash.com/photo6",
    )
    monster_image7 = Monster_image(
        monster_id=4, preview=True, url="https://images.unsplash.com/photo7",
    )
    monster_image8 = Monster_image(
        monster_id=4, preview=False, url="https://images.unsplash.com/photo8",
    )
    monster_image9 = Monster_image(
        monster_id=5, preview=True, url="https://images.unsplash.com/photo9",
    )
    monster_image10 = Monster_image(
        monster_id=5, preview=False, url="https://images.unsplash.com/photo10",
    )
    monster_image11 = Monster_image(
        monster_id=6, preview=True, url="https://images.unsplash.com/photo11",
    )
    monster_image12 = Monster_image(
        monster_id=6, preview=False, url="https://images.unsplash.com/photo12",
    )
    monster_image13 = Monster_image(
        monster_id=7, preview=True, url="https://images.unsplash.com/photo13",
    )
    monster_image14 = Monster_image(
        monster_id=7, preview=False, url="https://images.unsplash.com/photo14",
    )
    monster_image15 = Monster_image(
        monster_id=8, preview=True, url="https://images.unsplash.com/photo15",
    )
    monster_image16 = Monster_image(
        monster_id=8, preview=False, url="https://images.unsplash.com/photo16",
    )
    monster_image17 = Monster_image(
        monster_id=9, preview=True, url="https://images.unsplash.com/photo17",
    )
    monster_image18 = Monster_image(
        monster_id=9, preview=False, url="https://images.unsplash.com/photo18",
    )
    monster_image19 = Monster_image(
        monster_id=10, preview=True, url="https://images.unsplash.com/photo19",
    )
    monster_image20 = Monster_image(
        monster_id=10, preview=False, url="https://images.unsplash.com/photo20",
    )



    db.session.add(monster_image1)
    db.session.add(monster_image2)
    db.session.add(monster_image3)
    db.session.add(monster_image4)
    db.session.add(monster_image5)
    db.session.add(monster_image6)
    db.session.add(monster_image7)
    db.session.add(monster_image8)
    db.session.add(monster_image9)
    db.session.add(monster_image10)
    db.session.add(monster_image11)
    db.session.add(monster_image12)
    db.session.add(monster_image13)
    db.session.add(monster_image14)
    db.session.add(monster_image15)
    db.session.add(monster_image16)
    db.session.add(monster_image17)
    db.session.add(monster_image18)
    db.session.add(monster_image19)
    db.session.add(monster_image20)

    # Add other monster images here
    # Relationships




    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_monster_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.monster_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM monster_images"))

    db.session.commit()
