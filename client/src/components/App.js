import React, { useState, useEffect } from "react";
import { Routes, Route, Navigate } from 'react-router-dom';
import Signup from "./Signup";
import Login from "./Login";
import Logout from "./Logout";
import Navbar from "./Navbar";
import TripContainer from "./TripContainer";
import CreateTrip from "./CreateTrip";
import EditTrip from "./EditTrip";
import DestinationForm from "./DestinationForm";
import DestinationList from "./DestinationList";

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
          <Route
            path=":tripId/edit"
            element={loggedInUser ? <EditTrip /> : <Navigate to="/login" />}
          />
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
        <Route path="/trips/:tripId/destinations" element={<DestinationList />} />
        <Route path="/trips/:tripId/destinations/new" element={<DestinationForm />} />

      </Routes>
    </div>
  );
}

export default App;