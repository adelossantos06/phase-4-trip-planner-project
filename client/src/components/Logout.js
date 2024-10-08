import React from "react";
import { useNavigate } from 'react-router-dom';
import "./Navbar.css"

function Logout({ setLoggedInUser }) {
    const navigate = useNavigate();

    const handleLogout = () => {
        fetch('/logout', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((resp) => {
            if (resp.ok) {
                setLoggedInUser(null);
                navigate('/login');
            } else {
                console.error('Logout Failed.');
            }
        })
    };

    return (
        <button className="logout-button" onClick={handleLogout}>Logout</button>
    );
}

export default Logout;