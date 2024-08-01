import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useOutletContext } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

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
    })

    return (
        <div>
            <Formik
                initialValues={initialValues}
                validationSchema={validationSchema}
                onSubmit={(values, { resetForm }) => {
                    addTrip(values);
                    resetForm();
                    navigate('/trips');
                }}
            >
                {({ isSubmitting }) => (
                    <Form className="create-trip-form">
                        <div>
                            <label htmlFor="title">Title</label>
                            <Field name="title" type="text" placeholder="Trip Title" />
                            <ErrorMessage name="title" component="div" />
                        </div>
                        <div>
                            <label htmlFor="start_date">Start Date</label>
                            <Field name="start_date" type="date" />
                            <ErrorMessage name="start_date" component="div" />
                        </div>
                        <div>
                            <label htmlFor="end_date">End Date</label>
                            <Field name="end_date" type="date" />
                            <ErrorMessage name="end_date" component="div" />
                        </div>
                        <div>
                            <label htmlFor="description">Description</label>
                            <Field name="description" as="textarea" placeholder="Trip Description" />
                            <ErrorMessage name="description" component="div" />
                        </div>
                        <button type="submit" disabled={isSubmitting}>Create Trip</button>
                    </Form>
                )}
            </Formik>
        </div>
    )
}

export default CreateTrip;