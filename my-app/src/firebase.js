import {initializeApp} from 'firebase/app';
// import {signInWithEmailAndPassword, createUserWithEmailAndPassword, getAuth, signInWithPopup, GoogleAuthProvider, signOut} from "firebase/auth";
import { getDatabase, ref, push, child, onValue, val, get, set } from "firebase/database";

const firebaseConfig = {
  apiKey: "AIzaSyBb1s3xaRqk1JUGq88g5H9-oINz23Ca-uA",
  authDomain: "lab12-34dd3.firebaseapp.com",
  databaseURL: "https://lab12-34dd3-default-rtdb.firebaseio.com",
  projectId: "lab12-34dd3",
  storageBucket: "lab12-34dd3.appspot.com",
  messagingSenderId: "185579286263",
  appId: "1:185579286263:web:7b49551753c8bbc8806df2"
};
var app = initializeApp(firebaseConfig);
// const auth = getAuth();
let database = getDatabase(app);

const dataStorage = [];

export function getData() {
  onValue(ref(database), (snapshot) => {
    dataStorage.length = 0; 
    snapshot.forEach((item) => {
      dataStorage.push(item.val()); 
    });
  });
}

export { dataStorage };
