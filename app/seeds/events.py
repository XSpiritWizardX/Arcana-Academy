from app.models import db, Event, environment, SCHEMA
from sqlalchemy.sql import text


def seed_events():
    event1 = Event(
         name='Wand Festival', time="8pm", date="01/03/2026", description="Festival of wands starts in January and and ends in March. This festival is a celebration of the wand and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new wands and accessories."
    )
    event2 = Event(
         name='Potion Festival', time="8pm", date="01/03/2026", description="Festival of potions starts in January and and ends in March. This festival is a celebration of the potion and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new potions and accessories."
    )
    event3 = Event(
         name='Spell Festival', time="8pm", date="01/03/2026", description="Festival of spells starts in January and and ends in March. This festival is a celebration of the spell and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new spells and accessories."
    )
    event4 = Event(
         name='Monster Festival', time="8pm", date="01/03/2026", description="Festival of monsters starts in January and and ends in March. This festival is a celebration of the monster and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new monsters and accessories."
    )
    event5 = Event(
         name='Wizard Festival', time="8pm", date="01/03/2026", description="Festival of wizards starts in January and and ends in March. This festival is a celebration of the wizard and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new wizards and accessories."
    )
    event6 = Event(
         name='Dragon Festival', time="8pm", date="01/03/2026", description="Festival of dragons starts in January and and ends in March. This festival is a celebration of the dragon and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new dragons and accessories."
    )
    event7 = Event(
         name='Element Festival', time="8pm", date="01/03/2026", description="Festival of elements starts in January and and ends in March. This festival is a celebration of the element and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new elements and accessories."
    )
    event8 = Event(
         name='Magic Festival', time="8pm", date="01/03/2026", description="Festival of magic starts in January and and ends in March. This festival is a celebration of the magic and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new magic and accessories."
    )
    event9 = Event(
         name='Wizardry Festival', time="8pm", date="01/03/2026", description="Festival of wizardry starts in January and and ends in March. This festival is a celebration of the wizardry and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new wizardry and accessories."
    )
    event10 = Event(
         name='Sorcery Festival', time="8pm", date="01/03/2026", description="Festival of sorcery starts in January and and ends in March. This festival is a celebration of the sorcery and its power. It is a time for wizards to come together and share their knowledge and skills with one another. The festival includes competitions, demonstrations, and workshops, as well as opportunities to purchase new sorcery and accessories."
    )




    db.session.add(event1)
    db.session.add(event2)
    db.session.add(event3)
    db.session.add(event4)
    db.session.add(event5)
    db.session.add(event6)
    db.session.add(event7)
    db.session.add(event8)
    db.session.add(event9)
    db.session.add(event10)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_events():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.events RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM events"))

    db.session.commit()
