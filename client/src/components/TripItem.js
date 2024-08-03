import React from "react";
import { useNavigate } from "react-router-dom";
import "./TripItem.css";

function TripItem({ trip, handleDelete }) {
    const navigate = useNavigate();

    const handleUpdate = () => {
        navigate(`/trips/${trip.id}/edit`);
    };

    const handleDestinations = () => {
        navigate(`/trips/${trip.id}/destinations`);
    };

    return (
        <div className="trip-card-container">
            <div className="trip-card">
                <h2 className="trip-card-title">{trip.title}</h2>
                <p><strong>Start Date: </strong>{trip.start_date}</p>
                <p><strong>End Date:</strong> {trip.end_date}</p>
                <p><strong>Description:</strong> {trip.description}</p>
                <button className="trip-card-button" onClick={handleDestinations}>View/ Add Destinations</button>
                <button className="trip-card-button" onClick={handleUpdate}>Edit Trip Details</button>
                <button className="trip-card-button" onClick={handleDelete}>Delete Trip</button>
            </div>
        </div>
    );
}

export default TripItem;
