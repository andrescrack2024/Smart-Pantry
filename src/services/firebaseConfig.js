import { initializeApp } from 'firebase/app';
import { initializeFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyCu-0FJ6c-7mGU_2Qqn-7IHwRPLjgqm42Q",
  authDomain: "smart-pantry-e60df.firebaseapp.com",
  projectId: "smart-pantry-e60df",
  storageBucket: "smart-pantry-e60df.firebasestorage.app",
  messagingSenderId: "304884461444",
  appId: "1:304884461444:web:9f46180eadefce7161f7d1",
  measurementId: "G-M9Q4XQ64MT"
};

const app = initializeApp(firebaseConfig);

// Configuración limpia sin caché local persistente para evitar inconsistencias de cierre de sesión
const db = initializeFirestore(app, {});

const auth = getAuth(app);
export { db, auth };