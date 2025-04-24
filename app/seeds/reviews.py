from app.models import db, Review, environment, SCHEMA
from sqlalchemy.sql import text


def seed_reviews():
    review1 = Review(
        user_id=3, title='Good Wand', rating=4, description="This wand is great for casting spells. I love the design and the way it feels in my hand. The only downside is that it could be a bit more powerful.")
    review2 = Review(
        user_id=4, title='Great Wand', rating=5, description="This wand is amazing! It has a great design and works perfectly. I would definitely recommend it to anyone looking for a new wand.")
    review3 = Review(
        user_id=5, title='Average Wand', rating=3, description="This wand is okay. It works well enough, but I expected more from it. The design is nice, but it could be more powerful.")
    review4 = Review(
        user_id=6, title='Bad Wand', rating=2, description="This wand is not great. It feels cheap and doesn't work as well as I expected. I would not recommend it to anyone.")
    review5 = Review(
        user_id=7, title='Excellent Wand', rating=5, description="This wand is fantastic! It has a beautiful design and works perfectly. I would highly recommend it to anyone looking for a new wand.")
    review6 = Review(
        user_id=8, title='Poor Wand', rating=1, description="This wand is terrible. It feels cheap and doesn't work at all. I would not recommend it to anyone.")
    review7 = Review(
        user_id=9, title='Decent Wand', rating=3, description="This wand is decent. It works well enough, but I expected more from it. The design is nice, but it could be more powerful.")
    review8 = Review(
        user_id=10, title='Amazing Wand', rating=5, description="This wand is amazing! It has a great design and works perfectly. I would definitely recommend it to anyone looking for a new wand.")
    review9 = Review(
        user_id=11, title='Good Wand', rating=4, description="This wand is great for casting spells. I love the design and the way it feels in my hand. The only downside is that it could be a bit more powerful.")
    review10 = Review(
        user_id=12, title='Great Wand', rating=5, description="This wand is amazing! It has a great design and works perfectly. I would definitely recommend it to anyone looking for a new wand.")
    review11 = Review(
        user_id=13, title='Average Wand', rating=3, description="This wand is okay. It works well enough, but I expected more from it. The design is nice, but it could be more powerful.")
    review12 = Review(
        user_id=14, title='Bad Wand', rating=2, description="This wand is not great. It feels cheap and doesn't work as well as I expected. I would not recommend it to anyone.")

    db.session.add(review1)
    db.session.add(review2)
    db.session.add(review3)
    db.session.add(review4)
    db.session.add(review5)
    db.session.add(review6)
    db.session.add(review7)
    db.session.add(review8)
    db.session.add(review9)
    db.session.add(review10)
    db.session.add(review11)
    db.session.add(review12)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_reviews():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))

    db.session.commit()
