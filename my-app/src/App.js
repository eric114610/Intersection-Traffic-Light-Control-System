import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes} from 'react-router-dom';

import Home from './Home';
import Funcpage from './function';
import Func1page from './func1';
import Case from './case.js'
import Func2page from './func2';



function App() {
  return (
    <Router>
      <div className="App">


        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/another" element={<Funcpage />} />
          <Route path="/another1" element={<Func1page />} />
          <Route path="/another2" element={<Func2page />} />
          <Route path="/case" element={<Case />} />
          
        </Routes>

      </div>
    </Router>
  );
}

export default App;


