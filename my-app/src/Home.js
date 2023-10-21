import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'

function Home() {
    return (
        <div className="starting-page">
          <div className='background'></div>
          <div className="div">
            <div className="title">車流監控輔助系統</div>
            <div className='sub-title'>
              <Link to="/another">
                <button className='starting-button'>Tap to Start !!</button>
              </Link>
            </div>
          </div>
        </div>
      );
}


export default Home;
