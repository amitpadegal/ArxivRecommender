import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";
import firebaseConfig from "./firebaseConfig.json"; // imported object

// const firebaseConfig = {
//     apiKey: "AIzaSyB5hxIEztoCXz2w2UOyxKyP0EYrffDw0u0",
//     authDomain: "arxivrecommender.firebaseapp.com",
//     projectId: "arxivrecommender",
//     storageBucket: "arxivrecommender.firebasestorage.app",
//     messagingSenderId: "612483725245",
//     appId: "1:612483725245:web:e07c1e1bf12f1d304ac4d4"
//   };
  

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider, signInWithPopup, signOut };
