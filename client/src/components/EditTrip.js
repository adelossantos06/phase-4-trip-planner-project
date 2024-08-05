import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useOutletContext } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import "./EditTrip.css"

function EditTrip() {
    const { trips, updateTrip } = useOutletContext();
    const { tripId } = useParams();
    const navigate = useNavigate()

    const trip = trips.find(t => t.id === parseInt(tripId))


    const initialValues = {
        title: trip.title,
        start_date: trip.start_date,
        end_date: trip.end_date,
        description: trip.description
    }

    const validationSchema = Yup.object({
        title: Yup.string().required('Title is required'),
        start_date: Yup.date().required('Start Date is required'),
        end_date: Yup.date()
            .min(Yup.ref('start_date'), 'End date cannot be before start date')
            .required('End Date is required'),
        description: Yup.string().required('Description is required')
    })

    return (
        <div className="edit-trip-container">
            <h1>Edit Trip Details</h1>
            <Formik
                initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={(values) => {
                    updateTrip(tripId, values);
                    navigate('/trips')
                }}
            >
                <Form className="edit-trip-form" >
                    <div className="form-group">
                        <label htmlFor="title">Title:</label>
                        <Field name="title" type="text" placeholder="Trip Title" />
                        <ErrorMessage name="title" component="div" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="start_date">Start Date:</label>
                        <Field name="start_date" type="date" />
                        <ErrorMessage name="start_date" component="div" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="end_date">End Date:</label>
                        <Field name="end_date" type="date" />
                        <ErrorMessage name="end_date" component="div" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="description">Description:</label>
                        <Field name="description" as="textarea" placeholder="Trip Description" />
                        <ErrorMessage name="description" component="div" />
                    </div>
                    <button type="submit" className="submit-button" >Save Changes</button>
                </Form>
            </Formik>
        </div >
    )

}

export default EditTrip