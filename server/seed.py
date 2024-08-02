#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports


# Local imports
from models import Trip, Destination, User, Activity, UserDestinationAssociation
from config import db, app

if __name__ == '__main__':
   
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        db.session.query(User).delete()
        db.session.query(Trip).delete()
        db.session.query(Destination).delete()
        db.session.query(UserDestinationAssociation).delete()

        db.session.commit()

        

       
        
        

        