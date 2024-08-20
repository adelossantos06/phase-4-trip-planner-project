import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import ActivityForm from "./ActivityForm";
import { useNavigate } from "react-router-dom";
import "./DestinationCard.css"


function DestinationCard({ destinations }) {
    const { tripId } = useParams();
    const [isFavorite, setIsFavorite] = useState(false);
    const navigate = useNavigate();

    const handleActivity = () => {
        navigate(`/trips/${tripId}/destinations/${destinations.id}/activities/new`, {
            state: { destinations }
        });
    };


    useEffect(() => {
        fetch(`/trips/${tripId}/destinations/${destinations.id}/association`)
            .then(res => {
                if (res.ok) {
                    return res.json();
                }
                throw new Error('Failed to fetch favorite status');
            })
            .then(data => {

                setIsFavorite(data.is_favorite);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }, [tripId, destinations.id]);

    const handleFavorite = () => {
        const newFavoriteStatus = !isFavorite;

        fetch(`/trips/${tripId}/destinations/${destinations.id}/association`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_favorite: newFavoriteStatus })
        })
            .then(res => {
                if (res.ok) {
                    return res.json();
                }
                throw new Error('Failed to update favorite status');
            })
            .then(data => {
                setIsFavorite(data.is_favorite);

            })
            .catch(error => {
                console.error('Error:', error);
            });


    };


    return (
        <div>
            <div id="destination-card">
                <p><strong>City: </strong> {destinations.city}</p>
                <p><strong>State: </strong> {destinations.state}</p>
                <p><strong>Country: </strong> {destinations.country}</p>
                <p><strong>Time Zone: </strong> {destinations.time_zone}</p>
                <button
                    onClick={handleFavorite}
                    className="favorite-button"
                >
                    {isFavorite ? '❤️' : '♡'}
                </button>
                <button
                    onClick={handleActivity}
                    className="view-activity-button"
                >
                    Add/ View Activity
                </button>
            </div>

        </div>
    );
}

export default DestinationCard;