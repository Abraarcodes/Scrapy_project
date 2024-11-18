import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gradient-to-r from-blue-500 via-purple-600 to-pink-600 p-4 text-white fixed top-0 left-0 w-full z-10 shadow-lg shadow-blue-500/50 transition-all duration-300 ease-in-out">
      <div className="flex justify-between items-center max-w-screen-xl mx-auto">
        <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 hover:scale-105 transition-all duration-300 ease-in-out">
          Smart Procure
        </h1>
        <div className="space-x-6 flex items-center">
          {/* Dashboard Link */}
          <Link 
            to="/dashboard" 
            className="text-lg font-medium transition-colors duration-300 ease-in-out hover:text-yellow-300 hover:underline hover:underline-offset-4 transform hover:scale-110"
          >
            Dashboard
          </Link>

          {/* Search Link */}
          <Link 
            to="/search" 
            className="text-lg font-medium transition-colors duration-300 ease-in-out hover:text-yellow-300 hover:underline hover:underline-offset-4 transform hover:scale-110"
          >
            Search
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
