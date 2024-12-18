import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import QueryPage from './pages/QueryPage';
import Specifications from './pages/Specifications'
import './index.css';


function App() {
  return (
    <Router>
      <div className="flex min-h-screen">
        {/* <Sidebar /> */}
        <div className="flex-1">
          {/* <Navbar /> */}
          <Routes>
            <Route path="/" element={<QueryPage />} />
            <Route path="/specifications" element={<Specifications/>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
