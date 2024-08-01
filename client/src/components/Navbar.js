import React from "react"
import { NavLink } from 'react-router-dom';
import Logout from "./Logout";
import CreateTrip from "./CreateTrip";

function Navbar({ setLoggedInUser }) {
    return (
        <header>
            <h1>Trip Planner</h1>
            <nav>
                <NavLink to="/">All my Trips</NavLink>
                <NavLink to="/trips/create">Create a new trip</NavLink>
                <Logout setLoggedInUser={setLoggedInUser} />
            </nav>
        </header>
    )
}

export default Navbar;