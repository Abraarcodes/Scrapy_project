import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="fixed top-14 left-0 bg-gray-800 text-white w-1/3 md:w-1/4 lg:w-1/5 min-h-screen p-6">
      <h2 className="text-2xl font-semibold text-white mb-8">Features</h2>
      <ul className="space-y-4">
        <li>
          <Link
            to="/dashboard"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors">
            Dashboard 
          </Link>
        </li>
        <li>
          <Link
            to="/search"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            Search Products/Services
          </Link>
        </li>

        {/* New Product-Related Features */}
        <li>
          <Link
            to="/top-picks"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            Top Product Picks
          </Link>
        </li>
        <li>
          <Link
            to="/new-arrivals"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            New Arrivals
          </Link>
        </li>
        <li>
          <Link
            to="/best-deals"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            Best Deals & Offers
          </Link>
        </li>
        <li>
          <Link
            to="/product-categories"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            Product Categories
          </Link>
        </li>
        <li>
          <Link
            to="/trending-products"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            Trending Products
          </Link>
        </li>
        <li>
          <Link
            to="/recommended-for-you"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            Recommended for You
          </Link>
        </li>
        <li>
          <Link
            to="/seasonal-picks"
            className="block py-2 px-4 text-white hover:bg-blue-600 rounded-lg transition-colors"
          >
            Seasonal Picks
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
