// import React, { useState } from 'react';
// import axios from 'axios';

// export default function AdvancedProductSearch() {
//   const [searchParams, setSearchParams] = useState({
//     itemName: '',
//     itemType: '',
//     make: '',
//     model: '',
//     customSearch: '',
//   });

//   const [data, setData] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const handleInputChange = (e) => {
//     const { name, value } = e.target;
//     setSearchParams((prev) => ({ ...prev, [name]: value }));
//   };

//   const handleSubmit = async (e) => {
//   e.preventDefault();

//   // Combine all parameters into a single string joined by '+'
//   const searchString = Object.values(searchParams)
//     .filter((value) => value) // Exclude empty values
//     .join('+');

//   console.log("Search String:", searchString);

//   setLoading(true);
//   setError(null);
//   setData([]);

//   try {
//     // Send the search string directly as the query
//     // const response = await axios.get(`http://localhost:5000/scrape?query=${encodeURIComponent(searchString)}`);
//     const response = await axios.get(`http://localhost:5000/scrape`, {
//       params: { search: searchString },
//     });

//     console.log('Backend Response:', response.data); // Debugging response

//     if (Array.isArray(response.data)) {
//       setData(response.data);
//     } else {
//       setError('Unexpected response format from the backend');
//     }
//   } catch (err) {
//     setError(err.message || 'Error fetching data from the backend');
//   } finally {
//     setLoading(false);
//   }
// };



//   // Sample data for dropdowns
//   const itemNames = ['Laptop', 'Smartphone', 'Tablet', 'Desktop', 'Camera'];
//   const itemTypes = ['Electronics', 'Accessories', 'Peripherals'];
//   const makes = ['Apple', 'Samsung', 'Dell', 'HP', 'Lenovo'];
//   const models = ['XPS15','Model A', 'Model B', 'Model C', 'Model D', 'Model E'];

//   return (
//     <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
//       <div className="max-w-7xl mx-auto">
//         <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
//           Advanced Product Search
//         </h1>
//         <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-8">
//           <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4 mb-6">
//             {[
//               { name: 'itemName', label: 'Item Name', options: itemNames },
//               // { name: 'itemType', label: 'Item Type', options: itemTypes },
//               { name: 'make', label: 'Make', options: makes },
//               { name: 'model', label: 'Model', options: models },
//             ].map((field) => (
//               <div key={field.name}>
//                 <label
//                   htmlFor={field.name}
//                   className="block text-sm font-medium text-gray-700 mb-1"
//                 >
//                   {field.label}
//                 </label>
//                 <select
//                   id={field.name}
//                   name={field.name}
//                   value={searchParams[field.name]}
//                   onChange={handleInputChange}
//                   className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
//                 >
//                   <option value="">Select {field.label}</option>
//                   {field.options.map((option) => (
//                     <option key={option} value={option}>
//                       {option}
//                     </option>
//                   ))}
//                   <option value="custom">Custom</option>
//                 </select>
//               </div>
//             ))}
//           </div>
//           <div className="mb-6">
//             <label
//               htmlFor="customSearch"
//               className="block text-sm font-medium text-gray-700 mb-1"
//             >
//               Custom Search
//             </label>
//             <input
//               type="text"
//               id="customSearch"
//               name="customSearch"
//               value={searchParams.customSearch}
//               onChange={handleInputChange}
//               placeholder="Enter custom search terms..."
//               className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
//             />
//           </div>
//           <div className="flex justify-center">
//             <button
//               type="submit"
//               className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
//               disabled={loading}
//             >
//               {loading ? (
//                 <>
//                   <svg
//                     className="animate-spin h-5 w-5 text-white mr-2"
//                     xmlns="http://www.w3.org/2000/svg"
//                     fill="none"
//                     viewBox="0 0 24 24"
//                   >
//                     <circle
//                       className="opacity-25"
//                       cx="12"
//                       cy="12"
//                       r="10"
//                       stroke="currentColor"
//                       strokeWidth="4"
//                     ></circle>
//                     <path
//                       className="opacity-75"
//                       fill="currentColor"
//                       d="M4 12a8 8 0 018-8v8H4z"
//                     ></path>
//                   </svg>
//                   Searching...
//                 </>
//               ) : (
//                 'Search Products'
//               )}
//             </button>
//           </div>
//         </form>
//         <div className="mt-8 bg-white shadow-md rounded-lg p-8">
//           {error && <p className="text-red-500">{error}</p>}
//           {data.length > 0 ? (
//             <div>
//               <h2 className="text-xl font-semibold text-gray-900 mb-4">Search Results</h2>
//               <table className="table-auto w-full border-collapse border border-gray-300">
//                 <thead className="bg-indigo-100">
//                   <tr>
//                     <th className="px-4 py-2 border border-gray-300">Title</th>
//                     <th className="px-4 py-2 border border-gray-300">Price</th>
//                     <th className="px-4 py-2 border border-gray-300">Link</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {data.map((product, index) => (
//                     <tr key={index}>
//                       <td className="px-4 py-2 border border-gray-300">{product.title}</td>
//                       <td className="px-4 py-2 border border-gray-300">{product.price}</td>
//                       <td className="px-4 py-2 border border-gray-300">
//                         <a
//                           href={product.link}
//                           target="_blank"
//                           rel="noopener noreferrer"
//                           className="text-indigo-600 underline"
//                         >
//                           View
//                         </a>
//                       </td>
//                     </tr>
//                   ))}
//                 </tbody>
//               </table>
//             </div>
//           ) : (
//             !loading && <p className="text-gray-600">No results found.</p>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }





















import React, { useState } from 'react';
import axios from 'axios';

export default function AdvancedProductSearch() {
  const [searchParams, setSearchParams] = useState({
    itemName: '',
    make: '',
    model: '',
    customSearch: '',
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

    const searchString = Object.values(searchParams)
      .filter((value) => value)
      .join('+');

    console.log('Search String:', searchString);

    setLoading(true);
    setError(null);
    setData([]);

    try {
      const response = await axios.get(`http://localhost:5000/scrape`, {
        params: { search: searchString },
      });

      console.log('Backend Response:', response.data);

      // Combine results from all spiders
      const combinedData = [];
      Object.keys(response.data).forEach((spider) => {
        combinedData.push(
          ...response.data[spider].map((item) => ({
            ...item,
            source: spider, // Add source info
          }))
        );
      });

      setData(combinedData);
    } catch (err) {
      setError(err.message || 'Error fetching data from the backend');
    } finally {
      setLoading(false);
    }
  };

  // Sample data for dropdowns
  const itemNames = ['Laptop', 'Smartphone', 'Tablet', 'Desktop', 'Camera'];
  const makes = ['Apple', 'Samsung', 'Dell', 'HP', 'Lenovo'];
  const models = ['XPS15', 'Model A', 'Model B', 'Model C', 'Model D', 'Model E'];

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          Advanced Product Search
        </h1>
        <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-8">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4 mb-6">
            {[
              { name: 'itemName', label: 'Item Name', options: itemNames },
              { name: 'make', label: 'Make', options: makes },
              { name: 'model', label: 'Model', options: models },
            ].map((field) => (
              <div key={field.name}>
                <label
                  htmlFor={field.name}
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  {field.label}
                </label>
                <select
                  id={field.name}
                  name={field.name}
                  value={searchParams[field.name]}
                  onChange={handleInputChange}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                >
                  <option value="">Select {field.label}</option>
                  {field.options.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                  <option value="custom">Custom</option>
                </select>
              </div>
            ))}
          </div>
          <div className="mb-6">
            <label
              htmlFor="customSearch"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Custom Search
            </label>
            <input
              type="text"
              id="customSearch"
              name="customSearch"
              value={searchParams.customSearch}
              onChange={handleInputChange}
              placeholder="Enter custom search terms..."
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
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
                'Search Products'
              )}
            </button>
          </div>
        </form>
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
                  </tr>
                </thead>
                <tbody>
                  {data.map((product, index) => (
                    <tr key={index}>
                      <td className="px-4 py-2 border border-gray-300">{product.title}</td>
                      <td className="px-4 py-2 border border-gray-300">{product.price}</td>
                      <td className="px-4 py-2 border border-gray-300">{product.rating}</td>
                      <td className="px-4 py-2 border border-gray-300">{product.source}</td>
                      <td className="px-4 py-2 border border-gray-300">
                        <a
                          href={product.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-indigo-600 underline"
                        >
                          View
                        </a>
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
