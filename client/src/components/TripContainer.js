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

    const contextValue = { addTrip };

    return (
        <div>
            <h1>Trips</h1>
            <Outlet context={contextValue} />
            <div>
                {trips.map((trip, index) => {
                    return <TripItem key={trip.id} trip={trip} />;
                })}
            </div>
        </div>
    );
}

export default TripContainer;