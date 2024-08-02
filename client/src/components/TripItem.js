import React from "react";
import { useNavigate } from "react-router-dom";
import DestinationList from "./DestinationList";

function TripItem({ trip, handleDelete }) {
    const navigate = useNavigate()

    const handleUpdate = () => {
        navigate(`/trips/${trip.id}/edit`);
    }

    const handleDestinations = () => {
        navigate(`/trips/${trip.id}/destinations`)
    }

    return (
        <div className="trip-card">
            <h2 className="trip-card-title">{trip.title}</h2>
            <p><strong>Start Date: </strong>{trip.start_date}</p>
            <p><strong>End Date:</strong> {trip.end_date}</p>
            <p><strong>Description:</strong> {trip.description}</p>
            <button onClick={handleDestinations} >View/ Add Desitnations</button>
            <button onClick={handleUpdate}>Edit Trip Details</button>
            <button onClick={handleDelete} >Delete Trip</button>
        </div>

    );
}

export default TripItem;