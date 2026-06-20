import { useState } from "react";
import api from "../services/api";

function CropRecommendation() {
  const [formData, setFormData] = useState({
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
  });

  const [result, setResult] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const response = await api.post("/predict", formData);

    setResult(
      `🌾 Recommended Crop: ${response.data.recommended_crop}`
    );
  } catch (error) {
    console.error("API Error:", error);
    setResult("❌ Failed to connect backend");
  }
};

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow-lg">

        <h1 className="text-4xl font-bold text-green-700 mb-6">
          🌱 Crop Recommendation
        </h1>

        <form onSubmit={handleSubmit} className="grid md:grid-cols-2 gap-4">

          <input
            type="number"
            name="nitrogen"
            placeholder="Nitrogen (N)"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          <input
            type="number"
            name="phosphorus"
            placeholder="Phosphorus (P)"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          <input
            type="number"
            name="potassium"
            placeholder="Potassium (K)"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          <input
            type="number"
            name="temperature"
            placeholder="Temperature (°C)"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          <input
            type="number"
            name="humidity"
            placeholder="Humidity (%)"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          <input
            type="number"
            name="ph"
            placeholder="pH Value"
            onChange={handleChange}
            className="border p-3 rounded-lg"
          />

          <input
            type="number"
            name="rainfall"
            placeholder="Rainfall (mm)"
            onChange={handleChange}
            className="border p-3 rounded-lg md:col-span-2"
          />

          <button
            type="submit"
            className="bg-green-700 text-white py-3 rounded-lg md:col-span-2"
          >
            Predict Crop
          </button>

        </form>

        {result && (
          <div className="mt-6 p-4 bg-green-100 rounded-lg text-xl font-semibold text-green-800">
            {result}
          </div>
        )}

      </div>
    </div>
  );
}

export default CropRecommendation;