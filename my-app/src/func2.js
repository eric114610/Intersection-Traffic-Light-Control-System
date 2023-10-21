import React from 'react';
import { useState, useEffect } from 'react';
import './func2.css'

import {initializeApp} from 'firebase/app';
// import {signInWithEmailAndPassword, createUsesrWithEmailAndPassword, getAuth, signInWithPopup, GoogleAuthProvider, signOut} from "firebase/auth";
import { getDatabase, ref, push, child, onValue, val, get, set } from "firebase/database";

const firebaseConfig2 = {
    apiKey: "AIzaSyDurUQg6c7MENG1Ce7qIl-KNhlg0cSd-KU",
    authDomain: "nxp-2-889f2.firebaseapp.com",
    databaseURL: "https://nxp-2-889f2-default-rtdb.firebaseio.com",
    projectId: "nxp-2-889f2",
    storageBucket: "nxp-2-889f2.appspot.com",
    messagingSenderId: "972237774704",
    appId: "1:972237774704:web:f6619eb33767dfead9b9b5"
};
var app2 = initializeApp(firebaseConfig2, "other");
// const auth = getAuth();
let database2 = getDatabase(app2);

function Func2page(){

    const [TestSet] = useState([
        {id: 1, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:30"},
        {id: 2, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:40"},
        {id: 3, straightSignal: "red", lateralSignal: "green", time:"2023-09-22-10:22:40"},
        {id: 4, straightSignal: "green", lateralSignal: "red", time:"2023-09-22-10:22:40"},


    ])

    const [StatusSet, setStatusSet] = useState([
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

        onValue(ref(database2), (snapshot) => {
            newSatusSet.length = 0; 
            snapshot.forEach((item) => {
              newSatusSet.push(item.val()); 
            });
            setStatusSet(newSatusSet);
        });    
    }


    useEffect(() => {
        //console.log(StatusSet);
    }, [StatusSet])


    let len = StatusSet.length;
    console.log(len);

    let index = len;
    const foundData = StatusSet.find(item=>item.id==index)
    
    if(foundData) {
        console.log(foundData);
        return(
            <div className='func2Page'>
              <div className='title'><h1>紅燈秒數調整</h1></div>
              <div><img></img></div>
              <div className='situation'>{foundData.status}</div>
              <div class='d-flex justify-content-center align-items-center'>
                <div className='content'>直向燈號: {foundData.straightSignal}</div>
                <div style={{ width: '150px' }}></div>
                <div className='content'>橫向燈號: {foundData.lateralSignal}</div>
              </div> 

            </div>
        );

    }else{
        console.log('未找到數據')
    }


}

export default Func2page;