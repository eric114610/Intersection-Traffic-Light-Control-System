import React from 'react';
import { useState, useEffect } from 'react';
import './func1.css'

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

const Ref = ref(database, 'events');


function Func1page() {
    //getData();
    //console.log(dataStorage);
    const [testSet] = useState([
        {abc:{id: 1, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.10.12"},
        bcd:{id: 2, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.10.12"},
        aaa:{id: 3, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.10.12"},
        bbb:{id: 4, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.10.12"},
        ccc:{id: 5, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.10.12"}},
    ])

    const [CaseSet, setCaseSet] = useState([
        //{id: 1, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.10.12"},
        //{id: 2, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.11.12"},
        //{id: 3, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.12.12"},
        //{id: 4, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.12.12"},
        //{id: 5, carNumber: "NBX-3388", category: "speeding", time:"2023-10-18-23.13.12"},
    ])
    
    useEffect(() => {
        fetchData();
    }, [])

    const fetchData = async() => {
        let newCaseSet=[];

        onValue(Ref, (snapshot) => {
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

    /*
    var transformedArray = [];
    let dataObject = CaseSet[0];
    for (var key in dataObject) {
        if (dataObject.hasOwnProperty(key)) {
          transformedArray.push(dataObject[key]);
        }
      }

    //console.log(testSet);
    console.log(transformedArray);

    //const reversed_CaseSet = CaseSet.reverse();
    */
    return (

        <div className='func1Page'>
            <div className='title'>違規車輛取締</div>
            {
                CaseSet.map(ca =>
                    <div>
                        <a className="card" key={ca.id} type="button" href={"/case?index=" + ca.id}>
                            <p className="card-text">{ca.time}</p>
                        </a>
                    </div>
                    
                )
            }
        </div>

    )
}

export default Func1page;
