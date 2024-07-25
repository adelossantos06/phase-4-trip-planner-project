#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from models import Trip, Destination
from config import db, app

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        Trip.query.delete()
        Destination.query.delete()

        t1 = Trip(title="San Antonio Trip", description="Texas Roadtrip starting in SA", start_date="08/29/24", end_date="09/06/24")
        t2 = Trip(title="Seattle/Portland Trip", description="Trip to see family", start_date="09/29/24", end_date="10/06/24")

        db.session.add_all([t1, t2])
        db.session.commit()

        d1 = Destination(city="San Antonio", state="Texas", country="United States", time_zone="Central", trip_id=t1.id)
        d2 = Destination(city="Dallas", state="Texas", country="United States", time_zone="Central", trip_id=t1.id)
        d3 = Destination(city="Seattle", state="Washington", country="United States", time_zone="Pacific", trip_id=t2.id)

        db.session.add_all([d1, d2, d3])
        db.session.commit()
        