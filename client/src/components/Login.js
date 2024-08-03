import React from "react";
import "./Login.css"
import { useNavigate } from 'react-router-dom';
import { NavLink } from 'react-router-dom';
import { Formik, Field, Form } from 'formik';
import * as yup from 'yup';


function Login({ setLoggedInUser }) {

    const navigate = useNavigate();


    const loginSchema = yup.object().shape({
        username: yup.string().required('Username is required'),
        password: yup.string().required('Password is required')
    });

    const initialValues = {
        username: '',
        password: ''
    };

    const handleSubmit = (values, { setErrors, resetForm }) => {
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(values)
        })
            .then((resp) => {

                if (resp.ok) {
                    return resp.json().then((loggedInUser) => {
                        setLoggedInUser(loggedInUser);
                        navigate('/trips');
                        resetForm()
                    });
                } else {
                    return resp.json().then((error) => {
                        console.error('Server error:', error);
                        setErrors({ server: error.message });
                    });
                }
            })
            .catch((error) => {

                console.error('Network error:', error);
                setErrors({ server: 'Network error. Please try again later.' });
            });
    };

    return (
        <>
            <h2 className="login-h2">Login</h2>
            <div className="form-container">
                <Formik
                    initialValues={initialValues}
                    onSubmit={handleSubmit}
                    validationSchema={loginSchema}
                >
                    {({ errors }) => (
                        <Form className='form'>
                            <label htmlFor="username">Username:</label>
                            <Field name="username" type="text" placeholder="Username" />
                            {errors.username && <div>{errors.username}</div>}

                            <label htmlFor="password">Password:</label>
                            <Field name="password" type="password" placeholder="Password" />
                            {errors.password && <div>{errors.password}</div>}

                            {errors.server && <div>{errors.server}</div>}

                            <button className='login-submit-button' type="submit">Login</button>
                        </Form>
                    )}
                </Formik>
                <div className="signup">
                    <p>Don't have an account?</p>
                    <NavLink to="/signup">
                        <button className="login-signup-button" >Sign Up</button>
                    </NavLink>

                </div>
            </div>
        </>
    );
}

export default Login;