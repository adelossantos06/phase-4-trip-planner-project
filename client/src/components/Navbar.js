import React from "react"
import "./Navbar.css"
import { NavLink } from 'react-router-dom';
import Logout from "./Logout";


function Navbar({ setLoggedInUser }) {
    return (
        <header className="navbar-header" >
            <h1>Trip Planner</h1>
            <nav className="navbar-nav" >
                <NavLink to="/" className="nav-link" >My Trips</NavLink>
                <NavLink to="/trips/create" className="nav-link">Create Trip</NavLink>
                <Logout setLoggedInUser={setLoggedInUser} />
            </nav>
        </header>
    )
}

export default Navbar;