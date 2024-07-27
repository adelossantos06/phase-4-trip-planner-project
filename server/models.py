from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-trips.user', '-favoriteDestinations.user', '-trips', '-favoriteDestinations.destination.favoriteDestinations')


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)

    trips = db.relationship('Trip', back_populates='user')
    favoriteDestinations = db.relationship('FavoriteDestination', back_populates='user')

class Trip(db.Model, SerializerMixin):
    __tablename__ = 'trips'

    serialize_rules = ('-destinations.trip', '-user.trips', '-destinations', '-user.favoriteDestinations', '-activities.trip')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    destinations = db.relationship('Destination', back_populates='trip', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='trips')
    activities = db.relationship('Activity', back_populates='trip', cascade='all, delete-orphan')

class Destination(db.Model, SerializerMixin):
    __tablename__ = 'destinations'

    serialize_rules = ('-trip.destinations', '-trip', '-favoriteDestinations.destination', '-favoriteDestinations', '-activities.destination')

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    time_zone = db.Column(db.String)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))

    trip = db.relationship('Trip', back_populates='destinations')
    favoriteDestinations = db.relationship('FavoriteDestination', back_populates='destination')
    activities = db.relationship('Activity', back_populates='destination', cascade='all, delete-orphan')


class FavoriteDestination(db.Model, SerializerMixin):
    __tablename__ = 'favoriteDestinations'

    serialize_rules = ('-user.favoriteDestinations', '-destination.favoriteDestinations', '-user.trips', '-destination.trip', 'user_id', 'destination_id', 'is_favorite')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    is_favorite = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='favoriteDestinations')
    destination = db.relationship('Destination', back_populates='favoriteDestinations')

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-destination.activities)',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    trip = db.relationship('Trip', back_populates='activities')
    destination = db.relationship('Destination', back_populates='activities')