import React, { useState } from "react";
import { useParams } from "react-router-dom";

function DestinationCard({ destinations }) {
    const { tripId } = useParams();
    const [isFavorite, setIsFavorite] = useState(destinations.is_favorite);

    const handleFavorite = () => {
        const updatedFavoriteStatus = !isFavorite;

        fetch(`/trips/${tripId}/destinations/${destinations.id}/association`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_favorite: updatedFavoriteStatus })
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
            <div className="destination-card">
                <p><strong>City: </strong> {destinations.city}</p>
                <p><strong>State: </strong> {destinations.state}</p>
                <p><strong>Country: </strong> {destinations.country}</p>
                <p><strong>Time Zone: </strong> {destinations.time_zone}</p>
                <button
                    onClick={handleFavorite}
                    style={{
                        backgroundColor: isFavorite ? 'pink' : 'gray',
                        color: 'white',
                        padding: '10px 20px',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer'
                    }}
                >
                    {isFavorite ? '❤️' : '♡'}
                </button>
            </div>
        </div>
    );
}

export default DestinationCard;