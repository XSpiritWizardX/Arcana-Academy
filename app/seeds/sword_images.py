from app.models import db, Sword_image, environment, SCHEMA
from sqlalchemy.sql import text


def seed_sword_images():
    # Add monster images here
    sword_image1 = Sword_image(
        sword_id=1,  url="https://images.unsplash.com/photo1",
    )
    sword_image2 = Sword_image(
        sword_id=2,  url="https://images.unsplash.com/photo2",
    )
    sword_image3 = Sword_image(
        sword_id=3,  url="https://images.unsplash.com/photo3",
    )
    sword_image4 = Sword_image(
        sword_id=4,  url="https://images.unsplash.com/photo4",
    )
    sword_image5 = Sword_image(
        sword_id=5,  url="https://images.unsplash.com/photo5",
    )
    sword_image6 = Sword_image(
        sword_id=6,  url="https://images.unsplash.com/photo6",
    )
    sword_image7 = Sword_image(
        sword_id=5,  url="https://images.unsplash.com/photo7",
    )




    db.session.add(sword_image1)
    db.session.add(sword_image2)
    db.session.add(sword_image3)
    db.session.add(sword_image4)
    db.session.add(sword_image5)
    db.session.add(sword_image6)
    db.session.add(sword_image7)

    # Add other monster images here
    # Relationships




    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_sword_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.sword_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM sword_images"))

    db.session.commit()
