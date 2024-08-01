import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate } from 'react-router-dom';
import Signup from "./Signup";
import Login from "./Login";
import Logout from "./Logout";
import Navbar from "./Navbar";
import Trips from "./Trips";
import TripContainer from "./TripContainer";
import CreateTrip from "./CreateTrip";

function App() {
  const [loggedInUser, setLoggedInUser] = useState(null);

  useEffect(() => {
    fetch('/authorized')
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Not authorized');
        }
      })
      .then(user => {
        setLoggedInUser(user);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      {loggedInUser && <Navbar setLoggedInUser={setLoggedInUser} />}
      <Routes>
        <Route
          path="/signup"
          element={loggedInUser ? <Navigate to="/trips" /> : <Signup />}
        />
        <Route
          path="/trips"
          element={loggedInUser ? <TripContainer /> : <Navigate to="/login" />}
        >
          <Route path="create" element={<CreateTrip />} />
        </Route>
        <Route
          path="/login"
          element={loggedInUser ? <Navigate to="/trips" /> : <Login setLoggedInUser={setLoggedInUser} />}
        />
        <Route
          path="/logout"
          element={<Logout setLoggedInUser={setLoggedInUser} />}
        />
        <Route
          path="*"
          element={<Navigate to={loggedInUser ? "/trips" : "/login"} />}
        />
      </Routes>
    </div>
  );
}

export default App;