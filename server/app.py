
from flask import app, request, make_response
from flask_restful import Resource
from config import app, db, api
from models import Trip, Destination

import ipdb

@app.route('/trips', methods=["GET"])
def all_trips():
    trips = Trip.query.all()
    trip_list = [trip.to_dict() for trip in trips]
    return make_response(trip_list)

@app.route('/trips/<int:id>', methods=['PATCH', 'DELETE'])
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

if __name__ == '__main__':
    app.run(port=5555, debug=True)

