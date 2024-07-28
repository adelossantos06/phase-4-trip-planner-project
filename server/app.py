
from flask import app, request, make_response
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource
from config import app, db, api
from models import Trip, Destination, User, Activity, FavoriteDestination


class Trips(Resource):
    def get(self):
        trips = Trip.query.all()
        trip_list = [trip.to_dict() for trip in trips]
        return make_response(trip_list)
    
    def post(self):
        data = request.json
        title = data.get('title'),
        description = data.get('description'),
        start_date = data.get('start_date'),
        end_date = data.get('end_date'),
        user_id = data.get('user_id')

        if not title or user_id:
            return make_response({'error': 'Title and User ID are required'}, 400)

        new_trip = Trip(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id
        )

        db.session.add(new_trip)
        db.session.commit()

        return make_response(new_trip.to_dict(), 201)

api.add_resource(Trips, '/trips')


class TripResource(Resource):
    def get(self, id):
        trip = Trip.query.get(id)
        if not trip:
            return ({'error': 'Trip not found'}, 404)
        return make_response(trip.to_dict(), 200)

    def patch(self, id):
        trip = Trip.query.get(id)
        if not trip:
            return ({'error': 'Trip not found'}, 404)

        params = request.json
        for attr, value in params.items():
            setattr(trip, attr, value)
        
        db.session.commit()
        return make_response(trip.to_dict(), 200)

    def delete(self, id):
        trip = Trip.query.get(id)
        if not trip:
            return ({'error': 'Trip not found'}, 404)

        db.session.delete(trip)
        db.session.commit()
        return make_response('', 204)

api.add_resource(TripResource, '/trips/<int:id>')


class UserTripResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response({'error': 'User not found'}, 404)

        trips = [trip.to_dict() for trip in user.trips]
        return make_response(trips, 200)

api.add_resource(UserTripResource, '/users/<int:user_id>/trips')    


class UserFavoritesResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response({'error': 'User not found'}, 404)

        favorite_destinaitons = [
            fav.destination.to_dict() for fav in user.favoriteDestinations
        ]
        return make_response(favorite_destinaitons, 200)

    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response({'error': 'User not found'}, 404)

        params = request.json
        destination_id = params.get('destination_id')

        if not destination_id:
            return make_response({'error': 'Destination ID is required'}, 400)

        exisitng_favorite = FavoriteDestination.query.filter_by(user_id=user_id, destination_id=destination_id).first()
        if exisitng_favorite:
            return make_response({'error': 'Favorite already exists'}, 409)
        
        favorite = FavoriteDestination(user_id=user_id, destination_id=destination_id, is_favorite=True)
        db.session.add(favorite)
        db.session.commit()

        return make_response(favorite.to_dict())

api.add_resource(UserFavoritesResource, '/users/<int:user_id>/favorites')

class RemoveFavoriteDestination(Resource):
    def delete(self, user_id, destination_id):
        favorite = FavoriteDestination.query.filter_by(user_id=user_id, destination_id=destination_id).first()
        if not favorite:
            return make_response({'error': 'Favorite destination not found'}, 404)

        db.session.delete(favorite)
        db.session.commit()
        return make_response('', 204)

api.add_resource(RemoveFavoriteDestination, '/users/<int:user_id>/favorites/<int:destination_id>')


class ActivitiesByDestination(Resource):
    def get(self, destination_id):
        destination = Destination.query.get(destination_id)
        if not destination:
            return make_response({'error': 'Destination not found'}, 404)

        activities = [
            activity.to_dict() for activity in destination.activities
        ]
        return make_response(activities, 200)
    
    def post(self, destination_id):
        destination = Destination.query.get(destination_id)
        if not destination:
            return make_response({'error': 'Destination not found'}, 404)

        params = request.json
        name = params.get('name')
        description = params.get('description')
        trip_id = params.get('trip_id')

        if not name or not trip_id:
            return make_response({'error': 'Name and Trip ID are required'}, 400)

        activity = Activity(name=name, description=description, trip_id=trip_id, destination_id=destination_id)
        db.session.add(activity)
        db.session.commit()

        return make_response(activity.to_dict(), 201)

api.add_resource(ActivitiesByDestination, '/destinations/<int:destination_id>/activities')


class ActivityResource(Resource):
    def delete(self, id):
        activity = Activity.query.get(id)
        if not activity:
            return make_response({'error': 'Activity not found'}, 404)

        db.session.delete(activity)
        db.session.commit()
        return make_response('', 204)

api.add_resource(ActivityResource, '/activities/<int:id>')

class Users(Resource):
     def post(self):
        request_body = request.json
        try:
            user = User(username=request_body["username"], age=request_body['age'])

            db.session.add(user)
            db.session.commit()
        except IntegrityError as i_error:
            if 'UNIQUE constraint failed: users.username' in str(i_error.orig):
                return make_response({'error': 'Username must be unique'}, 422)
            elif 'CHECK constraint failed' in str(i_error.orig):
                return make_response({'error': 'Age must be greater than 15'}, 422)
            else:
                return make_response({'error': 'Database error'}, 500)
        except ValueError as v_error:
            return make_response({'error': str(v_error)}, 422)

        return make_response(user.to_dict(), 201)

api.add_resource(Users, '/users')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

