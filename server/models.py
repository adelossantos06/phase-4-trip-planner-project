from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db

class Trip(db.Model, SerializerMixin):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)

    destinations = db.relationship('Destination', back_populates='trip')

class Destination(db.Model, SerializerMixin):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    time_zone = db.Column(db.String)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))

    trip = db.relationship('Trip', back_populates='destinations')