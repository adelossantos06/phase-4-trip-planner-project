
from flask import app, request, make_response
from flask_restful import Resource
from config import app, db, api
from models import Trip

import ipdb
# Views go here!
@app.route('/trips', methods=["GET"])
def all_trips():
    trips = Trip.query.all()
    trip_list = [trip for trip in trips]
    ipdb.set_trace()
    print('hello')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

