import React, { useState, useEffect, useRef } from "react";
import { auth, provider, signInWithPopup, signOut } from "./firebase";
import { getIdToken } from "firebase/auth";
import RecommendedPapers from "./components/RecommendedPapers";

function App() {
  const [user, setUser] = useState(null);
  const [feedback, setFeedback] = useState({});
  const sentRef = useRef(false);
  const [papers, setPapers] = useState([]);

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
    await fetchPapers(user);
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
  
  const fetchPapers = async (user) => {
    try {
      const token = await user.getIdToken();
  
      const response = await fetch("http://localhost:8000/recommend", {
        headers: { Authorization: `Bearer ${token}` },
      });
  
      const data = await response.json();
      setPapers(data.papers.documents.map((doc, i) => ({
              id: data.papers.ids[i] || `paper-${i}`,
              title: data.papers.metadatas[i]?.title || "Untitled",
              authors: data.papers.metadatas[i]?.authors || "",
              published: data.papers.metadatas[i]?.published || "",
              abstract: doc,
            })));
    } catch (err) {
      console.error("❌ Failed to fetch:", err);
    }
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
          <RecommendedPapers feedback={feedback} setFeedback={setFeedback} papers={papers} setPapers = {setPapers} fetchPapers = {fetchPapers} />
        </>
      )}
    </div>
  );
}

export default App;
