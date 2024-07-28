from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-trips.user', '-favoriteDestinations.user', '-trips', '-favoriteDestinations.destination.favoriteDestinations')


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer)

    __table_args__ = (
        db.CheckConstraint('age > 15', name='check_age'),
    )

    trips = db.relationship('Trip', back_populates='user')

    destination_associations = db.relationship('UserDestinationAssociation', back_populates='user')
    destinations = association_proxy('destination_associations', 'destination')

    
    @validates('username')
    def validate_username(self, key, new_username):
        if len(new_username) < 2:
            raise ValueError('Username must be greater than 2 characters')
        return new_username

class Trip(db.Model, SerializerMixin):
    __tablename__ = 'trips'

    serialize_rules = ('-user.trips', '-destinations.trip', '-activities.trip')


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    destinations = db.relationship('Destination', back_populates='trip', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='trips')
    activities = db.relationship('Activity', back_populates='trip', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'user_id': self.user_id
        }

class Destination(db.Model, SerializerMixin):
    __tablename__ = 'destinations'

    serialize_rules = ('-trip.destinations', '-favoriteDestinations.destination')

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    country = db.Column(db.String)
    time_zone = db.Column(db.String)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

    trip = db.relationship('Trip', back_populates='destinations')
    activities = db.relationship('Activity', back_populates='destination', cascade='all, delete-orphan')

    user_associations = db.relationship('UserDestinationAssociation', back_populates='destination')
    users = association_proxy('user_associations', 'user')

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'time_zone': self.time_zone,
            'trip_id': self.trip_id
        }

class UserDestinationAssociation(db.Model):
    __tablename__ = 'user_destination_association'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), primary_key=True)

    user = db.relationship("User", back_populates="destination_associations")
    destination = db.relationship("Destination", back_populates="user_associations")

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-trip.activities', '-destination.activities')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)

    trip = db.relationship('Trip', back_populates='activities')
    destination = db.relationship('Destination', back_populates='activities')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'trip_id': self.trip_id,
            'destination_id':self.destination_id
        }
