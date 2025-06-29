import React, { useEffect, useState } from "react";
import { getAuth } from "firebase/auth";
import { auth } from "../firebase.js"; // your firebase.js setup

export default function RecommendedPapers({ feedback, setFeedback }) {
  const [papers, setPapers] = useState([]);

  // Fetch recommended papers
  useEffect(() => {
    const fetchPapers = async () => {
      const user = auth.currentUser;
      if (!user) return;
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
    };

    fetchPapers();
  }, []);
  

  // Handle like / dislike
  const handleFeedback = (paperId, value) => {
    console.log(paperId, value);
    console.log(feedback);
    setFeedback((prev) => ({ ...prev, [paperId]: value }));
  };

  return (
    <div>
      <h2>Recommended Papers</h2>
      {papers.map((paper) => (
        <div
          key={paper.id}
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "16px",
            margin: "12px 0",
          }}
        >
          <h3>{paper.title}</h3>
          <p>{paper.abstract}</p>
          <button
            style={{ marginRight: "8px" }}
            onClick={() => handleFeedback(paper.id, 1)}
          >
            👍 Like
          </button>
          <button onClick={() => handleFeedback(paper.id, -1)}>👎 Dislike</button>
        </div>
      ))}
    </div>
  );
}
