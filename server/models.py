from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-trips.user', '-destination_associations.user', '-destinations.user_associations' , '-destinations.trip', '-trips.destinations', '-destination_associations.destinations', '-destinations.users')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.CheckConstraint('age > 15', name='check_age'),
    )

    trips = db.relationship('Trip', back_populates='user')

    destination_associations = db.relationship('UserDestinationAssociation', back_populates='user')
    destinations = association_proxy('destination_associations', 'destination')

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        byte_object = password.encode('utf-8')
        bcrypt_hash = bcrypt.generate_password_hash(byte_object)
        hash_object_as_string = bcrypt_hash.decode('utf-8')
        self._password_hash = hash_object_as_string

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, new_username):
        if len(new_username) < 2:
            raise ValueError('Username must be greater than 2 characters')
        return new_username

class Trip(db.Model, SerializerMixin):
    __tablename__ = 'trips'

    serialize_rules = ('-user.trips', '-destinations.trip')


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    destinations = db.relationship('Destination', back_populates='trip', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='trips')
    # activities = db.relationship('Activity', back_populates='trip', cascade='all, delete-orphan')

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

    serialize_rules = ('-trip.destinations', '-user_associations.destination', '-users.destination_associations', '-user_associations.user.destination_associations', '-trip.user')


    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String)
    country = db.Column(db.String)
    time_zone = db.Column(db.String)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

    trip = db.relationship('Trip', back_populates='destinations')
    activities = db.relationship('Activity', back_populates='destination', cascade='all, delete-orphan')

    user_associations = db.relationship('UserDestinationAssociation', back_populates='destination', cascade='all, delete-orphan')
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

class UserDestinationAssociation(db.Model, SerializerMixin):
    __tablename__ = 'user_destination_association'

    serialize_rules = ('-user.destination_associations', '-destination.user_associations', '-user.destinations', '-destinations.users' )


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), primary_key=True)
    is_favorite = db.Column(db.Boolean, nullable=False, default=True)

    user = db.relationship("User", back_populates="destination_associations")
    destination = db.relationship("Destination", back_populates="user_associations")

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'destination_id': self.destination_id,
            'is_favorite': self.is_favorite
        }

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ( '-destination.activities', '-destination.trip')


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    order = db.Column(db.Integer)

    destination = db.relationship('Destination', back_populates='activities')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'destination_id':self.destination_id,
            'order': self.order
        }
