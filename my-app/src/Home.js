import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'
import VideoBackground from './VideoBackground';

function Home() {
    return (
        <div className="starting-page">
          <VideoBackground></VideoBackground>
          <div className="div">
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
