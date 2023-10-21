import React from 'react';
import { useLocation } from 'react-router-dom';
import queryString from 'query-string';
import { useState, useEffect } from 'react';
import './case.css'

//import { dataStorage, getData } from './firebase';

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



function Case() {
    const [CaseSet, setCaseSet] = useState([
        {id: 1, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.10.12"},
        {id: 2, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.11.12"},
        {id: 3, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.12.12"},
        {id: 4, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.12.12"},
        {id: 5, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.13.12"},
    ])
    
    useEffect(() => {
        fetchData();
    }, [])

    const fetchData = async() => {
        let newCaseSet=[];

        onValue(ref(database), (snapshot) => {
            newCaseSet.length = 0; 
            snapshot.forEach((item) => {
              newCaseSet.push(item.val()); 
            });
            setCaseSet(newCaseSet);
        });

        
    }

    useEffect(() => {
        console.log(CaseSet);
    }, [CaseSet])  
  //getData();
  //console.log(dataStorage);    
  let location = useLocation();
  let params = queryString.parse(location.search);
  let index = params.index;

  
  const foundData = CaseSet.find(item=>item.id==index)

  if (foundData) {
    console.log(foundData);
    return(
        <div className='content'>
            <div>Case: {foundData.id}</div>
            <br></br>
            <div>Time: {foundData.time}</div>
            <br></br>
            <div>Category: {foundData.category}</div>
            <br></br>
            <div>CarNumber: {foundData.carNumber}</div>
            
        </div>
      )
  } else {
    console.log('未找到数据');
  }
    
}

export default Case;