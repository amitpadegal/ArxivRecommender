import React, { useState, useEffect, useRef } from "react";
import { auth, provider, signInWithPopup, signOut } from "./firebase";
import { getIdToken } from "firebase/auth";
import RecommendedPapers from "./components/RecommendedPapers";

function App() {
  const [user, setUser] = useState(null);
  const [feedback, setFeedback] = useState({});
  const sentRef = useRef(false);

  const sendFeedback = async () => {
    if (sentRef.current || Object.keys(feedback).length === 0) return;
    sentRef.current = true;

    const user = auth.currentUser;
    if (!user) return;
    console.log(feedback);
    const token = await user.getIdToken();
    await fetch("http://localhost:8000/feedback", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ feedback }),
    });
  };

  const getRecommendations = async () => {
    console.log("Sending feedback");
    await sendFeedback(); // 🔁 flush feedback
  };

  const handleLogout = async () => {
    console.log("Sending feedback");
    await sendFeedback(); // 🔁 flush feedback
    await auth.signOut(); // 🚪 logout
  };

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(async (user) => {
      if (!user) {
        await sendFeedback();
      }
    });

    return () => unsubscribe();
  }, [feedback]);


  const handleLogin = async () => {
    const result = await signInWithPopup(auth, provider);
    setUser(result.user);
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
          <button onClick={getRecommendations}>Get Recommendations</button>
          <RecommendedPapers feedback={feedback} setFeedback={setFeedback} />
        </>
      )}
    </div>
  );
}

export default App;
