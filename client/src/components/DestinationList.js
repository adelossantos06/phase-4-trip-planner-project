import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function DestinationList() {
    const [destinations, setDestinations] = useState([]);
    const { tripId } = useParams();

    useEffect(() => {
        fetch(`/trips/${tripId}/destinations`)
            .then(resp => resp.json())
            .then(data => setDestinations(data))
            .catch(error => console.error('Error fetching destinations:', error));
    }, [tripId])


    return (
        <div>

        </div>
    )
}

export default DestinationList;