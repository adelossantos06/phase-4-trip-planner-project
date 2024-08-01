import React, { useEffect, useState } from "react";
import { Outlet } from 'react-router-dom';
import TripItem from "./TripItem";

function TripContainer() {
    const [trips, setTrips] = useState([]);

    useEffect(() => {
        fetch('/trips')
            .then((resp) => resp.json())
            .then((data) => {
                console.log('Fetched trips:', data);
                setTrips(data);
            })
            .catch((error) => console.error('Error fetching trips:', error));
    }, []);

    const addTrip = (newTrip) => {
        fetch('/trips', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newTrip),
        })
            .then((resp) => resp.json())
            .then((data) => {
                setTrips((prevTrips) => [...prevTrips, data]);
            })
            .catch((error) => console.error('Error creating trip:', error));
    };

    const updateTrip = (trip_id, updatedData) => {
        fetch(`/trips/${trip_id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData),
        })
            .then((resp) => resp.json())
            .then((updatedTrip) => {
                setTrips((prevTrips) => prevTrips.map(trip =>
                    trip.id === updatedTrip.id ? updatedTrip : trip
                ));
            })
            .catch((error) => console.error('Error updating trip:', error));
    };

    const handleDelete = (trip_id) => {
        fetch(`/trips/${trip_id}`, {
            method: 'DELETE'
        })
            .then((resp) => {
                if (resp.ok) {
                    setTrips(trips.filter(trip => trip.id !== trip_id));
                } else {
                    console.error('Failed to delete the trip');
                }
            })
            .catch((error) => console.error('Error deleting trip:', error));
    }

    const contextValue = { trips, addTrip, updateTrip, handleDelete };

    return (
        <div>
            <h1>Trips</h1>
            <Outlet context={contextValue} />
            <div>
                {trips.map((trip) => {
                    return <TripItem
                        key={trip.id}
                        trip={trip}
                        handleDelete={() => handleDelete(trip.id)}
                    />;
                })}
            </div>
        </div>
    );
}

export default TripContainer;