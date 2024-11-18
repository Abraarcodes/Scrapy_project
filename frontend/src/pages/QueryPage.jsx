import React, { useState } from 'react';
import axios from 'axios';

const QueryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchClick = async () => {
  setLoading(true);
  setError(null);

  try {
    const response = await axios.get(`http://localhost:5000/scrape`, {
      params: { search: searchQuery },
    });

    console.log(response.data); // Log response for debugging
    if (Array.isArray(response.data)) {
      setData(response.data);
    } else {
      setError('Unexpected data format');
    }
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">Product Scraper</h1>
      <div className="w-full max-w-md">
        <input
          type="text"
          placeholder="Enter product name"
          value={searchQuery}
          onChange={handleSearchChange}
          className="border p-2 w-full mb-2"
        />
        <button
          onClick={handleSearchClick}
          className="bg-blue-500 text-white px-4 py-2 rounded w-full"
          disabled={loading}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {data.length > 0 && (
        <table className="table-auto mt-4 border-collapse border border-gray-300 bg-white shadow-md">
          <thead className="bg-blue-100">
            <tr>
              <th className="px-4 py-2 border border-gray-300">Title</th>
              <th className="px-4 py-2 border border-gray-300">Price</th>
              <th className="px-4 py-2 border border-gray-300">Link</th>
            </tr>
          </thead>
          <tbody>
            {data.map((product, index) => (
              <tr key={index}>
                <td className="px-4 py-2 border border-gray-300">{product.title}</td>
                <td className="px-4 py-2 border border-gray-300">{product.price}</td>
                <td className="px-4 py-2 border border-gray-300">
                  <a href={product.link} target="_blank" rel="noopener noreferrer" className="text-blue-600">
                    View
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default QueryPage;
