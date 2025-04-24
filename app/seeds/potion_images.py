from app.models import db, Potion_image, environment, SCHEMA
from sqlalchemy.sql import text


def seed_potion_images():
    # Add monster images here
    potion_image1 = Potion_image(
        potion_id=1,  url="https://images.unsplash.com/photo1",
    )
    potion_image2 = Potion_image(
        potion_id=2,  url="https://images.unsplash.com/photo2",
    )
    potion_image3 = Potion_image(
        potion_id=3,  url="https://images.unsplash.com/photo3",
    )
    potion_image4 = Potion_image(
        potion_id=4,  url="https://images.unsplash.com/photo4",
    )
    potion_image5 = Potion_image(
        potion_id=5,  url="https://images.unsplash.com/photo5",
    )
    potion_image6 = Potion_image(
        potion_id=6,  url="https://images.unsplash.com/photo6",
    )
    potion_image7 = Potion_image(
        potion_id=5,  url="https://images.unsplash.com/photo7",
    )
    potion_image8 = Potion_image(
        potion_id=4,  url="https://images.unsplash.com/photo8",
    )
    potion_image9 = Potion_image(
        potion_id=3,  url="https://images.unsplash.com/photo9",
    )
    potion_image10 = Potion_image(
        potion_id=1,  url="https://images.unsplash.com/photo10",
    )





    db.session.add(potion_image1)
    db.session.add(potion_image2)
    db.session.add(potion_image3)
    db.session.add(potion_image4)
    db.session.add(potion_image5)
    db.session.add(potion_image6)
    db.session.add(potion_image7)
    db.session.add(potion_image8)
    db.session.add(potion_image9)
    db.session.add(potion_image10)

    # Add other monster images here
    # Relationships




    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_potion_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.potion_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM potion_images"))

    db.session.commit()
