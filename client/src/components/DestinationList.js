import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import DestinationForm from "./DestinationForm";
import DestinationCard from "./DestinationCard";
import "./DestinationList.css"

function DestinationList() {
    const [destinations, setDestinations] = useState([]);
    const { tripId } = useParams();

    const fetchDestinations = async () => {
        const response = await fetch(`/trips/${tripId}/destinations`);
        const data = await response.json();
        setDestinations(data);
    };


    useEffect(() => {
        fetchDestinations();
    }, []);

    const handleDestinationAdded = () => {
        fetchDestinations();
    };




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
        <div >

            <DestinationForm tripId={tripId} onDestinationAdded={handleDestinationAdded} />
            <h2 className="destination-h2">Destinations</h2>
            <div className="destination-list-container"  >
                <div className="destination-cards" >
                    {destinations.map((destination) => (
                        <DestinationCard
                            key={destination.id}
                            destinations={destination}
                        />
                    ))}
                </div>
            </div>
            {destinations.length == 0 && (
                <p className="no-destinations" >No Destinations Yet</p>
            )}

        </div >
    );
}

export default DestinationList;