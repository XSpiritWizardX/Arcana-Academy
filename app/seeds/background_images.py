from app.models import db, Background_image, environment, SCHEMA
from sqlalchemy.sql import text


def seed_background_images():
    bg_image1 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image2 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image3 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image4 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image5 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image6 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image7 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image8 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image9 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )
    bg_image10 = Background_image(
        url="https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGJhY2tncm91bmR8ZW58MHx8fHwxNjg5NTQ1NzA3&ixlib=rb-4.0.3&q=80&w=1080",
    )

    db.session.add(bg_image1)
    db.session.add(bg_image2)
    db.session.add(bg_image3)
    db.session.add(bg_image4)
    db.session.add(bg_image5)
    db.session.add(bg_image6)
    db.session.add(bg_image7)
    db.session.add(bg_image8)
    db.session.add(bg_image9)
    db.session.add(bg_image10)
    # Add other background images here



    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_background_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.background_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM background_images"))

    db.session.commit()
