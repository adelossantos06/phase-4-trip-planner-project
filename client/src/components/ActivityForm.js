import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useNavigate } from "react-router-dom";
import * as Yup from 'yup';
import { useLocation } from "react-router-dom";
import ActivityCard from "./ActivityCard";
import "./ActivityForm.css"

function ActivityForm() {
    const { destinationId, tripId } = useParams();
    const [activities, setActivities] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    const { destinations } = location.state || {};

    useEffect(() => {
        fetch(`/destinations/${destinationId}/activities`)
            .then(response => response.json())
            .then(data => setActivities(data))
            .catch(error => console.error('Error fetching activities:', error));
    }, [destinationId]);

    const initialValues = {
        name: '',
        description: '',
        destinationId: destinationId
    };

    const validationSchema = Yup.object({
        name: Yup.string().required('Name is required'),
        description: Yup.string().required('Description is required'),
    });

    const handleSubmit = (values, { resetForm }) => {
        fetch(`/destinations/${destinationId}/activities`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(values),
        })
            .then(resp => {
                if (resp.ok) {
                    return resp.json();
                }
                throw new Error('Failed to add activity');
            })
            .then(newActivity => {
                setActivities(prevActivities => {
                    const updatedActivities = [...prevActivities, newActivity];
                    console.log("Updated Activities:", updatedActivities); // Debugging log
                    return updatedActivities;
                });
                resetForm();
            })

            .catch(error => console.error('Error adding activity:', error));
    };

    if (!destinations) {
        return <div>No destination data available.</div>;
    }

    return (
        <div  >
            <div className="activity-form-container" >
                <h2>Activity for {destinations.city}, {destinations.state}</h2>
                <Formik
                    initialValues={initialValues}
                    validationSchema={validationSchema}
                    onSubmit={handleSubmit}
                >
                    <Form className="activity-form" >
                        <div>
                            <label htmlFor="name">Name</label>
                            <Field name="name" type="text" />
                            <ErrorMessage name="name" component="div" />
                        </div>

                        <div>
                            <label htmlFor="description">Description</label>
                            <Field name="description" as="textarea" />
                            <ErrorMessage name="description" component="div" />
                        </div>

                        <button
                            type="submit"

                        >Add Activity
                        </button>
                    </Form>
                </Formik>
            </div>
            <div>
                <h2>Activities</h2>
                {activities.length > 0 ? (
                    activities.map((activity, index) => (
                        <ActivityCard key={index} activities={activity} />
                    ))
                ) : (
                    <p>No activities yet.</p>
                )}
            </div>
        </div>
    );
}

export default ActivityForm;