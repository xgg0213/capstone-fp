from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_users():
    try:
        demo = User(
            username='Demo',
            first_name='Demo',
            last_name='User',
            email='demo@aa.io',
            password='password',
            balance=100000.00  # Start with $100k
        )
        marnie = User(
            username='marnie',
            first_name='Marnie',
            last_name='Smith',
            email='marnie@aa.io',
            password='password',
            balance=50000.00  # Start with $50k
        )
        bobbie = User(
            username='bobbie',
            first_name='Bobbie',
            last_name='Johnson',
            email='bobbie@aa.io',
            password='password',
            balance=75000.00  # Start with $75k
        )

        db.session.add(demo)
        db.session.add(marnie)
        db.session.add(bobbie)
        db.session.commit()
        print('Users seeded successfully!')
    except Exception as e:
        db.session.rollback()
        print('Error seeding users:', str(e))
        raise e


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
    db.session.commit()
    print('Users table cleared!')
