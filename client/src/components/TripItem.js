import React from "react";

function TripItem({ trip }) {
    return (
        <div className="trip-card">
            <h2 className="trip-card-title">{trip.title}</h2>
            <p><strong>Start Date: </strong>{trip.start_date}</p>
            <p><strong>End Date:</strong> {trip.end_date}</p>
            <p><strong>Description:</strong> {trip.description}</p>
        </div>
    );
}

export default TripItem;