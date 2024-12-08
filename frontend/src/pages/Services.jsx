import React, { useState } from "react";
import axios from "axios";

export default function AdvancedServiceSearch() {
  const [searchParams, setSearchParams] = useState({
    service: "",
    location: "",
  });

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const searchString = `${searchParams.service}+${searchParams.location}`;
    console.log("Search String:", searchString);

    setLoading(true);
    setError(null);
    setData([]);

    try {
      const response = await axios.get(`http://localhost:5000/scrape`, {
        params: { search: searchString },
      });

      console.log("Backend Response:", response.data);

      const combinedData = response.data.map((item) => ({
        ...item,
        source: item.source || "Unknown", // Optional: Add default source
      }));

      setData(combinedData);
    } catch (err) {
      setError(err.message || "Error fetching data from the backend");
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async (service) => {
    try {
      console.log("Sending purchase data:", {
        title: service.title,
        price: service.price,
        link: service.url,
      });

      const response = await axios.post("http://localhost:5000/save-purchase", {
        title: service.title,
        price: service.price,
        link: service.url,
      });

      if (response.data.success) {
        alert("Service saved for future benchmarking!");
      } else {
        alert("Error saving service data.");
      }
    } catch (error) {
      console.error("Error saving purchase:", error);
      alert("Error saving purchase.");
    }
  };

  const services = ["Electricity", "Security", "Water", "Cleaning", "Maintenance"];

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          Advanced Service Search
        </h1>
        <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-8">
          <div className="grid grid-cols-1 gap-6 mb-6">
            {/* Service Dropdown */}
            <div>
              <label
                htmlFor="service"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Select Service
              </label>
              <select
                id="service"
                name="service"
                value={searchParams.service}
                onChange={handleInputChange}
                className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
              >
                <option value="">Select a Service</option>
                {services.map((service) => (
                  <option key={service} value={service}>
                    {service}
                  </option>
                ))}
              </select>
            </div>

            {/* Location Input */}
            <div>
              <label
                htmlFor="location"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Location
              </label>
              <input
                type="text"
                id="location"
                name="location"
                value={searchParams.location}
                onChange={handleInputChange}
                placeholder="Enter location..."
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </div>
          </div>

          <div className="flex justify-center">
            <button
              type="submit"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg
                    className="animate-spin h-5 w-5 text-white mr-2"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v8H4z"
                    ></path>
                  </svg>
                  Searching...
                </>
              ) : (
                "Search Services"
              )}
            </button>
          </div>
        </form>

        {/* Results Section */}
        <div className="mt-8 bg-white shadow-md rounded-lg p-8">
          {error && <p className="text-red-500">{error}</p>}
          {data.length > 0 ? (
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Search Results</h2>
              <table className="table-auto w-full border-collapse border border-gray-300">
                <thead className="bg-indigo-100">
                  <tr>
                    <th className="px-4 py-2 border border-gray-300">Title</th>
                    <th className="px-4 py-2 border border-gray-300">Price</th>
                    <th className="px-4 py-2 border border-gray-300">Rating</th>
                    <th className="px-4 py-2 border border-gray-300">Source</th>
                    <th className="px-4 py-2 border border-gray-300">Link</th>
                    <th className="px-4 py-2 border border-gray-300">Purchase</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((service, index) => (
                    <tr key={index}>
                      <td className="px-4 py-2 border border-gray-300">{service.title}</td>
                      <td className="px-4 py-2 border border-gray-300">{service.price}</td>
                      <td className="px-4 py-2 border border-gray-300">{service.rating}</td>
                      <td className="px-4 py-2 border border-gray-300">{service.source}</td>
                      <td className="px-4 py-2 border border-gray-300">
                        <a
                          href={service.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-indigo-600 underline"
                        >
                          View
                        </a>
                      </td>
                      <td className="px-4 py-2 border border-gray-300">
                        <button
                          onClick={() => handlePurchase(service)}
                          className="px-4 py-2 bg-green-500 text-white rounded-md"
                        >
                          Purchase
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            !loading && <p className="text-gray-600">No results found.</p>
          )}
        </div>
      </div>
    </div>
  );
}
