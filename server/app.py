
from flask import Flask, request, make_response, session,jsonify
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource
from config import app, db, api
from models import Trip, Destination, User, UserDestinationAssociation, Activity
import bcrypt

class Trips(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized'}, 401)

        trips = Trip.query.filter_by(user_id=user_id).all()
        trip_list = [trip.to_dict() for trip in trips]
        return make_response(trip_list, 200)
    
    def post(self):
        data = request.json
        title = data.get('title')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        user_id = session.get('user_id')
        if not title or not user_id:
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
        if not trip or trip.user_id != session.get('user_id'):
            return make_response({'error': 'Trip not found or unauthorized'}, 404)
        return make_response(trip.to_dict(), 200)

    def patch(self, id):
        trip = Trip.query.get(id)
        if not trip or trip.user_id != session.get('user_id'):
            return make_response({'error': 'Trip not found or unauthorized'}, 404)

        params = request.json
        for attr, value in params.items():
            setattr(trip, attr, value)
        
        db.session.commit()
        return make_response(trip.to_dict(), 200)

    def delete(self, id):
        trip = Trip.query.get(id)
        if not trip or trip.user_id != session.get('user_id'):
            return make_response({'error': 'Trip not found or unauthorized'}, 404)

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

class DestinationsByTrip(Resource):
    def get(self, trip_id):
        trip = Trip.query.get(trip_id)
        if not trip:
            return make_response({'error': 'Trip not found'}, 404)

        destinations = [destination.to_dict() for destination in trip.destinations]
        return make_response(jsonify(destinations), 200) 

    def post(self, trip_id):
        user_id = session.get('user_id')
        trip = Trip.query.get(trip_id)
        if not trip:
            return make_response(jsonify({'error': 'Trip not found'}), 404)

        data = request.json
        if not data:
            return make_response(jsonify({'error': 'Invalid input'}), 400)
        
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')
        time_zone = data.get('time_zone')

        if not all([city, state, country, time_zone]):
            return make_response(jsonify({'error': 'Missing required fields'}), 400)

        new_destination = Destination(
            city=city,
            state=state,
            country=country,
            time_zone=time_zone,
            trip_id=trip_id
        )

        try:
            db.session.add(new_destination)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)

        if user_id:
            try:
                association = UserDestinationAssociation(
                    user_id=user_id,
                    destination_id=new_destination.id,
                    is_favorite=False 
                )
                db.session.add(association)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return make_response(jsonify({'error': str(e)}), 500)

        return make_response(jsonify({'message': 'Destination added and associated successfully'}), 201)

api.add_resource(DestinationsByTrip, '/trips/<int:trip_id>/destinations')



class UserDestinationAssociationResource(Resource):
    def get(self, trip_id, destination_id):
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized'}, 401)

        association = UserDestinationAssociation.query.filter_by(user_id=user_id, destination_id=destination_id).first()
        if not association:
            return make_response({'error': 'Association not found'}, 404)

        return make_response({'is_favorite': association.is_favorite}, 200)

    def patch(self, trip_id, destination_id):
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized'}, 401)

        destination = Destination.query.filter_by(id=destination_id, trip_id=trip_id).first()
        if not destination:
            return make_response({'error': 'Destination not found'}, 404)

        association = UserDestinationAssociation.query.filter_by(user_id=user_id, destination_id=destination_id).first()
        if not association:
            return make_response({'error': 'Association not found'}, 404)

        data = request.json
        is_favorite = data.get('is_favorite')
        if is_favorite is not None:
            association.is_favorite = is_favorite
            db.session.commit()
            return make_response({'message': 'Favorite status updated successfully', 'is_favorite': association.is_favorite}, 200)
        else:
            return make_response({'error': 'Invalid data'}, 400)
api.add_resource(UserDestinationAssociationResource, '/trips/<int:trip_id>/destinations/<int:destination_id>/association')



class ActivitiesByDestination(Resource):
    def get(self, destination_id):
        destination = Destination.query.get(destination_id)
        if not destination:
            return make_response({'error': 'Destination not found'}, 404)

        activities = Activity.query.filter_by(destination_id=destination_id).order_by(Activity.order).all()
        activities_dict = [activity.to_dict() for activity in activities]
        
        return make_response(activities_dict, 200)
    
    def post(self, destination_id):
        destination = Destination.query.get(destination_id)
        if not destination:
            return make_response({'error': 'Destination not found'}, 404)

        params = request.json
        name = params.get('name')
        description = params.get('description')
        

        if not name:
            return make_response({'error': 'Name required'}, 400)

        activity = Activity(name=name, description=description, destination_id=destination_id)
        db.session.add(activity)
        db.session.commit()

        return make_response(activity.to_dict(), 201)

api.add_resource(ActivitiesByDestination, '/destinations/<int:destination_id>/activities')

class ReorderActivities(Resource):
    def patch(self, destination_id):
        data = request.json
        activity_order = data.get('activities')

        if not activity_order:
            return make_response({'error': 'Invalid input data'}, 400)

        try:
            for index, activity_data in enumerate(activity_order):
                activity = Activity.query.get(activity_data['id'])
                if activity and activity.destination_id == destination_id:
                    activity.order = index
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)

        return make_response({'message': 'Activities reordered successfully'}, 200)

api.add_resource(ReorderActivities, '/destinations/<int:destination_id>/activities/reorder')



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
            user.password_hash = request_body['password']
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
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

class Login(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        
        if not user:
            return make_response({'error': 'Invalid username'}, 404)
        
        stored_hash = user.password_hash.encode('utf-8') if isinstance(user.password_hash, str) else user.password_hash
        provided_password = data['password'].encode('utf-8')
        
        if bcrypt.checkpw(provided_password, stored_hash):
            session['user_id'] = user.id
            return make_response(user.to_dict(), 200)
        else:
            return make_response({'error': 'Invalid username or password'}, 401)

api.add_resource(Login, '/login')

class Authorized(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return make_response(user.to_dict(), 200)
            else:
                return make_response({'error': 'User not found'}, 404)
        else:
            return make_response({'error': 'Unauthorized'}, 401)

api.add_resource(Authorized, '/authorized')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return make_response({}, 204)

api.add_resource(Logout, '/logout')

@app.before_request
def check_authorized():
    if request.endpoint == 'authorized' and not session.get('user_id'):
        return make_response({'error': 'Unauthorized'}, 401)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

