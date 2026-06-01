import { db } from './firebaseConfig';
import { collection, addDoc, query, orderBy, Timestamp, onSnapshot, doc, updateDoc, where } from 'firebase/firestore';

// Ahora la colección depende del ID de la familia
const getPantryRef = (familyId) => collection(db, 'pantries', familyId, 'items');

export const addFoodItem = async (familyId, name, daysLeft, category = "Otros", quantity = "1 unid", image = null) => {
  const today = new Date();
  const expDate = new Date(today);
  expDate.setDate(today.getDate() + daysLeft); 

  return await addDoc(getPantryRef(familyId), {
    name, daysLeft, category, quantity,
    status: daysLeft <= 0 ? 'expired' : (daysLeft <= 2 ? 'expiring_soon' : 'fresh'),
    active: true,
    purchaseDate: Timestamp.fromDate(today),
    expirationDate: Timestamp.fromDate(expDate),
    image
  });
};

export const consumeFoodItem = async (familyId, itemId) => {
  const itemDoc = doc(db, 'pantries', familyId, 'items', itemId);
  return await updateDoc(itemDoc, { active: false, consumedAt: Timestamp.now() });
};

export const subscribeToFamilyPantry = (familyId, callback) => {
  const q = query(getPantryRef(familyId), where("active", "==", true), orderBy('daysLeft', 'asc'));
  return onSnapshot(q, (querySnapshot) => {
    const items = [];
    querySnapshot.forEach((doc) => items.push({ id: doc.id, ...doc.data() }));
    callback(items);
  });
};