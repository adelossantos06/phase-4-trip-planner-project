import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Formik, Field, Form } from 'formik';
import * as yup from 'yup';

function Signup() {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    const signupSchema = yup.object().shape({
        username: yup.string().min(2, 'Username is too Short!').required('Username is required'),
        password: yup.string().min(5, 'Password is too Short!').required('Password is required'),
        age: yup.number().min(16, 'Age must be at least 16').required('Age is required')
    });

    const initialValues = {
        username: '',
        password: '',
        age: ''
    };

    const handleSubmit = (values, { setSubmitting, setErrors, resetForm }) => {
        fetch('/users', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(values)
        }).then((resp) => {
            setSubmitting(false);
            if (resp.ok) {
                resp.json().then((user) => {
                    setUser(user);
                    // TODO: Navigate to sign in
                    navigate('/login');
                    resetForm()
                });
            } else {
                resp.json().then((error) => {
                    setErrors({ server: error.message });
                    console.log('Server error:', error);
                });
                console.log('error');
            }
        }).catch((error) => {
            setSubmitting(false);
            console.log(error);
        });
    };

    return (
        <>
            <h2>Signup</h2>
            <div>
                <Formik
                    initialValues={initialValues}
                    onSubmit={handleSubmit}
                    validationSchema={signupSchema}
                >
                    {({ isSubmitting, errors }) => (
                        <Form className="signup-form">
                            <label htmlFor="username">Username:</label>
                            <Field name="username" type="text" placeholder="Username" />
                            {errors.username && <div>{errors.username}</div>}

                            <label htmlFor="password">Password:</label>
                            <Field name="password" type="password" placeholder="Password" />
                            {errors.password && <div>{errors.password}</div>}

                            <label htmlFor="age">Age:</label>
                            <Field name="age" type="number" placeholder="Age" />
                            {errors.age && <div>{errors.age}</div>}

                            {errors.server && <div>{errors.server}</div>}

                            <button type="submit" disabled={isSubmitting}>
                                {isSubmitting ? 'Submitting...' : 'Submit'}
                            </button>
                        </Form>
                    )}
                </Formik>
            </div>
        </>
    );
}

export default Signup;