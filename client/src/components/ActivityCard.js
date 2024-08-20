import React from "react";
import "./ActivityCard.css"

function ActivityCard({ activities }) {
    return (
        <>

            <div className="activity-card-container">
                <div className="activity-card">
                    <h2 className="activity-card-title">{activities.name}</h2>
                    <p><strong>Description: </strong>{activities.description}</p>
                </div>
            </div>
        </>

    );
}

export default ActivityCard;