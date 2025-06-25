import React, { useState, useEffect } from "react";
import { auth, provider, signInWithPopup, signOut } from "./firebase";
import { getIdToken } from "firebase/auth";

function App() {
  const [user, setUser] = useState(null);

  const handleLogin = async () => {
    const result = await signInWithPopup(auth, provider);
    setUser(result.user);
  };

  const handleLogout = () => {
    signOut(auth);
    setUser(null);
  };

  const handleGetToken = async () => {
    if (!auth.currentUser) return;
    const token = await getIdToken(auth.currentUser, true); // Firebase JWT
    console.log("Firebase JWT:", token);

    // Send token to backend
    const response = await fetch("http://localhost:8000/recommend", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(data);
  };

  return (
    <div>
      <h1>📚 Arxiv Recommender</h1>
      {!user ? (
        <button onClick={handleLogin}>Login with Google</button>
      ) : (
        <>
          <p>Welcome, {user.displayName}</p>
          <button onClick={handleLogout}>Logout</button>
          <button onClick={handleGetToken}>Get Recommendations</button>
        </>
      )}
    </div>
  );
}

export default App;
