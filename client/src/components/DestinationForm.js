import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import "./DestinationForm.css"

function DestinationForm({ onDestinationAdded }) {

    const navigate = useNavigate();
    const { tripId } = useParams();


    const initialValues = {
        city: '',
        state: '',
        country: '',
        time_zone: '',
    };

    const validationSchema = Yup.object({
        city: Yup.string().required('City is required'),
        state: Yup.string().required('State is required'),
        country: Yup.string().required('Country is required'),
        time_zone: Yup.string().required('Time Zone is required')
    });

    const handleSubmit = (values, { resetForm }) => {
        fetch(`/trips/${tripId}/destinations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(values),
        })
            .then(resp => {
                if (resp.ok) {
                    onDestinationAdded()
                    resetForm();
                    navigate(`/trips/${tripId}/destinations`);
                }
            })
            .catch(error => console.error('Error adding destinations:', error));
    };

    return (
        <div className="destination-form-container" >
            <h1>Add Destination</h1>
            <Formik
                initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={handleSubmit}
            >

                <Form className="destination-form" >
                    <div className="form-group">
                        <label htmlFor="city">City:</label>
                        <Field name="city" type="text" />
                        <ErrorMessage name="city" component="div" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="state">State:</label>
                        <Field name="state" type="text" />
                        <ErrorMessage name="state" component="div" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="country">Country:</label>
                        <Field name="country" type="text" />
                        <ErrorMessage name="country" component="div" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="time_zone">Time Zone:</label>
                        <Field name="time_zone" type="text" />
                        <ErrorMessage name="time_zone" component="div" />
                    </div>
                    <button className="submit-button" type="submit">Submit</button>
                </Form>

            </Formik>
        </div>
    );
}

export default DestinationForm;