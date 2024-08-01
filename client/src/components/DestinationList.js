import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DestinationForm from "./DestinationForm";

function DestinationList() {
    const [destinations, setDestinations] = useState([]);
    const { tripId } = useParams();

    useEffect(() => {
        fetch(`/trips/${tripId}/destinations`)
            .then(resp => {
                if (resp.ok) {
                    return resp.json();
                }
                throw new Error('Failed to fetch destinations');
            })
            .then(data => setDestinations(data))
            .catch(error => console.error('Error fetching destinations:', error));
    }, [tripId]);

    return (
        <div>
            <h2>Destinations</h2>
            <ul>
                {destinations.map(destination => (
                    <li key={destination.id}>
                        {destination.city}, {destination.state}, {destination.country}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default DestinationList;