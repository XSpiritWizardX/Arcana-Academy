from app.models import db, Schedule, environment, SCHEMA
from sqlalchemy.sql import text


def seed_schedules():
    schedule1 = Schedule(
        user_id=3, event_id=1,  description="Schedule for event 1"
    )
    schedule2 = Schedule(
        user_id=3, event_id=2,  description="Schedule for event 2"
    )
    schedule3 = Schedule(
        user_id=3, event_id=3,  description="Schedule for event 3"
    )
    schedule4 = Schedule(
        user_id=3, event_id=4,  description="Schedule for event 4"
    )
    schedule5 = Schedule(
        user_id=3, event_id=5,  description="Schedule for event 5"
    )
    schedule6 = Schedule(
        user_id=3, event_id=6,  description="Schedule for event 6"
    )
    schedule7 = Schedule(
        user_id=3, event_id=7,  description="Schedule for event 7"
    )
    schedule8 = Schedule(
        user_id=3, event_id=8,  description="Schedule for event 8"
    )
    schedule9 = Schedule(
        user_id=3, event_id=9,  description="Schedule for event 9"
    )
    schedule10 = Schedule(
        user_id=1, event_id=10,  description="Schedule for event 10"
    )
    schedule11 = Schedule(
        user_id=1, event_id=11,  description="Schedule for event 11"
    )
    schedule12 = Schedule(
        user_id=1, event_id=12,  description="Schedule for event 12"
    )
    schedule13 = Schedule(
        user_id=1, event_id=13,  description="Schedule for event 13"
    )
    schedule14 = Schedule(
        user_id=1, event_id=14,  description="Schedule for event 14"
    )
    schedule15 = Schedule(
        user_id=1, event_id=15,  description="Schedule for event 15"
    )
    db.session.add(schedule1)
    db.session.add(schedule2)
    db.session.add(schedule3)
    db.session.add(schedule4)
    db.session.add(schedule5)
    db.session.add(schedule6)
    db.session.add(schedule7)
    db.session.add(schedule8)
    db.session.add(schedule9)
    db.session.add(schedule10)
    db.session.add(schedule11)
    db.session.add(schedule12)
    db.session.add(schedule13)
    db.session.add(schedule14)
    db.session.add(schedule15)
    # Add other stages here


    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_schedules():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.schedules RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM schedules"))

    db.session.commit()
