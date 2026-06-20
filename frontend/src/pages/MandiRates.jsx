import { useState } from "react";
import api from "../services/api";

function MandiRates() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);

  const getRates = async () => {
    try {
      const response = await api.get(`/mandi/${city}`);
      setData(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-2xl shadow-lg">

        <h1 className="text-4xl font-bold text-green-700 mb-6">
          📈 Mandi Rates
        </h1>

        <input
          type="text"
          placeholder="Enter City Name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="w-full border p-3 rounded-lg mb-4"
        />

        <button
          onClick={getRates}
          className="w-full bg-green-700 text-white py-3 rounded-lg"
        >
          Get Mandi Rates
        </button>

        {data && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">
              📍 {data.city} Mandi Rates
            </h2>

            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-green-700 text-white">
                  <th className="border p-3">Crop</th>
                  <th className="border p-3">Price (₹/Quintal)</th>
                </tr>
              </thead>

              <tbody>
                {data.crops.map((crop, index) => (
                  <tr key={index}>
                    <td className="border p-3">{crop.name}</td>
                    <td className="border p-3">₹ {crop.price}</td>
                  </tr>
                ))}
              </tbody>
            </table>

          </div>
        )}

      </div>
    </div>
  );
}

export default MandiRates;