import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useOutletContext } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import "./CreateTrip.css"

function CreateTrip() {
    const { addTrip } = useOutletContext();
    const navigate = useNavigate();
    const initialValues = {
        title: '',
        start_date: '',
        end_date: '',
        description: '',
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
        <div className="create-trip-container" >
            <Formik
                initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={(values, { resetForm }) => {
                    addTrip(values);
                    resetForm();
                    navigate('/trips');
                }}
            >

                <Form className="create-trip-form">
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
                    <button type="submit" className="submit-button" >Create Trip</button>
                </Form>

            </Formik>
        </div>
    )
}

export default CreateTrip;