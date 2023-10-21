import React from 'react';
import { Link } from 'react-router-dom';
import './function.css'



function Funcpage() {
  return (
    <div className='funcpage'>
      <div className='background'></div>
      <div className='d-flex justify-content-center align-items-center' style={{ height: '50vh' }}>
          <Link to="/another1">
            <button className='square-button'>違規車輛取締</button>
          </Link>
          
          <div style={{ width: '150px' }}></div>
          <Link to="/another2">
            <button className='square-button'>紅燈秒數調整</button>
          </Link>
        
      </div>
    </div>
  );
}

export default Funcpage;
