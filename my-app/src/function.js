import React from 'react';
import { Link } from 'react-router-dom';
import './function.css'



function Funcpage() {
  return (
    <div className='funcpage'>
      <div className='background'></div>
      <div className='my-container d-flex justify-content-center align-items-center' style={{ height: '100vh' }}>
        <div>
            <Link to="/another1">
                <button class="image-button">
                    <img src={`${process.env.PUBLIC_URL}/violation.png`} alt="violation.png" />
                </button>
            </Link>
            <div class="text-box">違規車輛取締</div>
        </div>
          
          
        <div style={{ width: '150px' }}></div>
        <div>
            <Link to="/another2">
                <button class="image-button">
                    <img src={`${process.env.PUBLIC_URL}/light.png`} alt="light.png" />
                </button>
            </Link>
            <div class="text-box">紅燈秒數調整</div>
        </div>
      </div>
    </div>
  );
}

export default Funcpage;
