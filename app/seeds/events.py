from app.models import db, Event, environment, SCHEMA
from sqlalchemy.sql import text


def seed_events():
    event1 = Event(
         name='Wand Festival', time="8pm", date="01/03/2026", description="Festival of wands starts in January and and ends in ."
    )
    event2 = Event(
         name='Potion Festival', time="8pm", date="01/03/2026", description="Festival of potions starts in January and and ends in Marc."
    )
    event3 = Event(
         name='Spell Festival', time="8pm", date="01/03/2026", description="Festival of spells starts in January and and ends in Ma."
    )
    event4 = Event(
         name='Monster Festival', time="8pm", date="01/03/2026", description="Festival of monsters starts in January and and ends in March.."
    )
    event5 = Event(
         name='Wizard Festival', time="8pm", date="01/03/2026", description="Festival of wizards starts in January and and ends in Marc."
    )
    event6 = Event(
         name='Dragon Festival', time="8pm", date="01/03/2026", description="Festival of dragons starts in January and and ends in Marc."
    )
    event7 = Event(
         name='Element Festival', time="8pm", date="01/03/2026", description="Festival of elements starts in January and and ends in March.."
    )
    event8 = Event(
         name='Magic Festival', time="8pm", date="01/03/2026", description="Festival of magic starts in January and and ends in M."
    )
    event9 = Event(
         name='Wizardry Festival', time="8pm", date="01/03/2026", description="Festival of wizardry starts in January and and ends in March. ."
    )
    event10 = Event(
         name='Sorcery Festival', time="8pm", date="01/03/2026", description="Festival of sorcery starts in January and and ends in March."
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
