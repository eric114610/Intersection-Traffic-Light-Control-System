import React from 'react';
import { useState, useEffect } from 'react';
import './func2.css'


import {initializeApp} from 'firebase/app';
// import {signInWithEmailAndPassword, createUsesrWithEmailAndPassword, getAuth, signInWithPopup, GoogleAuthProvider, signOut} from "firebase/auth";
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

const Ref = ref(database, 'light');
const Ref1 = ref(database, 'test_sumo_light');


function Func2page(){

    const [TestSet] = useState([
        {id: 1, situation: "NS_Straight_Green", time:"2023-09-22-10:22:30"},
        {id: 2, situation: "NS_Straight_Green", time:"2023-09-22-10:22:40"},
        {id: 3, situation: "NS_Straight_Green", time:"2023-09-22-10:22:40"},
        {id: 4, situation: "NS_Straight_Green", time:"2023-09-22-10:22:40"},


    ])

    const [StatusSet, setStatusSet] = useState([
        //{id: 1, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:30"},
        //{id: 2, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:40"},
        //{id: 3, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:40"},

    ])

    const [lightSet, setlightSet] = useState([
        //{id: 1, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:30"},
        //{id: 2, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:40"},
        //{id: 3, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:40"},

    ])

    useEffect(() => {
        fetchData(); // 初始
    
        const intervalId = setInterval(() => {
            fetchData(); 
        }, 10000);
    
        
        return () => clearInterval(intervalId);
    }, []);

    const fetchData = async() => {
        let newSatusSet=[];
        let newlightSet=[];

        onValue(Ref, (snapshot) => {
            newSatusSet.length = 0; 
            snapshot.forEach((item) => {
              newSatusSet.push(item.val()); 
            });
            setStatusSet(newSatusSet);
        });
        
        onValue(Ref1, (snapshot) => {
            newlightSet.length = 0; 
            snapshot.forEach((item) => {
              newlightSet.push(item.val()); 
            });
            setlightSet(newlightSet);
        });  
    }


    useEffect(() => {
        console.log(StatusSet);
    }, [StatusSet])

    useEffect(() => {
        console.log(lightSet);
    }, [lightSet])



    let light = lightSet[0];
    console.log(light);
    
    
        
    return(
        <div className='func2Page'>
          <div className='title'><h1>紅燈秒數調整</h1></div>
          <div>{light}</div>
          
            <table>
                <thead>
                    <tr className='headrow'>
                        <th className='centered'>ID</th>
                        <th className='centered'>Time</th>
                        <th className='centered'>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {StatusSet.map(item => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{item.time}</td>
                        <td>{item.situation}</td>
                    </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );

  


}

export default Func2page;