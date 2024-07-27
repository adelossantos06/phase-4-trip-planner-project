
from flask import app, request, make_response
from flask_restful import Resource
from config import app, db, api
from models import Trip, Destination, User

import ipdb

@app.route('/trips', methods=["GET"])
def all_trips():
    trips = Trip.query.all()
    trip_list = [trip.to_dict(rules=('-destinations',)) for trip in trips]
    return make_response(trip_list)

@app.route('/trips/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def trip_by_id(id):
    trip = Trip.query.get(id)
    if request.method == 'PATCH':
        params = request.json

        for attr in params:
            setattr(trip, attr, params[attr])

        db.session.commit()

        return make_response(trip.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(trip)
        db.session.commit()

        return make_response('', 204)
    elif request.method == 'GET':
        return make_response(trip.to_dict())

@app.route('/users/<int:user_id>/favorites', methods=['GET', 'POST'])
def user_favorite_destinations(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response({'error': 'User not found'}, 404)

    if request.method == 'GET':
        favorite_destinaitons = [
            fav.destination.to_dict(rules=('-favoriteDestinations',)) for fav in user.favoriteDestinations
        ]
        return make_response(favorite_destinaitons)

    elif request.method == 'POST':
        params = request.join
        destination_id = params.get('destination_id')

        if not destination_id:
            return make_response({'error': 'Destination ID is required'}, 400)
        
        favorite = FavoriteDestination(user_id=user_id, destination_id=destination_id, is_favorite=True)
        db.session.add(favorite)
        db.session.commit()

        return make_response(favorite.to_dict(), 200)

@app.route('/users/<int:user_id>/favorites/<int:destination_id>', methods=['DELETE'])
def delete_favorite_destination(user_id, destination_id):
    favorite = FavoriteDestination.query.filter_by(user_id=user_id, destination_id=destination_id).first()
    if not favorite:
        return make_response({'error': 'Favorite destination not found'}, 404)

    db.session.delete(favorite)
    db.session.commit()

    return make_response('', 204)



if __name__ == '__main__':
    app.run(port=5555, debug=True)

