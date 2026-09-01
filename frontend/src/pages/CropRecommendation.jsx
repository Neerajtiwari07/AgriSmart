import { useState } from "react";
import api from "../services/api";
import Location from "../components/Location";

function CropRecommendation() {
  const [locationData, setLocationData] = useState({
    state: "",
    district: "",
    sub_district: "",
  });

  const [formData, setFormData] = useState({
    soil_type: "medium",
    month: new Date().getMonth() + 1,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // -----------------------------
  // Location Change
  // -----------------------------
  const handleLocationChange = (data) => {
    setLocationData(data);
    setResult(null);
  };

  // -----------------------------
  // Form Change
  // -----------------------------
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    setResult(null);
  };

  // -----------------------------
  // Submit
  // -----------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!locationData.state) {
      setResult({
        success: false,
        message: "Please select a state.",
      });
      return;
    }

    if (!locationData.district) {
      setResult({
        success: false,
        message: "Please select a district.",
      });
      return;
    }

    if (!locationData.sub_district) {
      setResult({
        success: false,
        message: "Please select a sub-district.",
      });
      return;
    }

    try {
      setLoading(true);
      setResult(null);

      /*
        Backend currently expects "location".
        We send district as the weather-search location.
      */

      const response = await api.post(
        "/smart-crop/predict",
        {
          location: locationData.district,
          soil_type: formData.soil_type,
          month: Number(formData.month),
        }
      );

      console.log("Smart Crop Response:", response.data);

      setResult(response.data);

    } catch (error) {
      console.error("Crop Recommendation Error:", error);

      setResult({
        success: false,
        message:
          error.response?.data?.message ||
          "❌ Failed to connect to backend.",
      });

    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Months
  // -----------------------------
  const months = [
    { value: 1, name: "January" },
    { value: 2, name: "February" },
    { value: 3, name: "March" },
    { value: 4, name: "April" },
    { value: 5, name: "May" },
    { value: 6, name: "June" },
    { value: 7, name: "July" },
    { value: 8, name: "August" },
    { value: 9, name: "September" },
    { value: 10, name: "October" },
    { value: 11, name: "November" },
    { value: 12, name: "December" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 p-6">

      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="text-center mb-8">

          <h1 className="text-4xl font-bold text-green-700">
            🌱 Smart Crop Recommendation
          </h1>

          <p className="text-gray-600 mt-2">
            Get the best crop recommendation using your location,
            soil type and current weather.
          </p>

        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">

          <form
            onSubmit={handleSubmit}
            className="space-y-6"
          >

            {/* -------------------------------- */}
            {/* Location Component */}
            {/* -------------------------------- */}

            <Location
              onLocationChange={handleLocationChange}
            />

            {/* -------------------------------- */}
            {/* Soil Type */}
            {/* -------------------------------- */}

            <div>

              <label className="block text-gray-700 font-semibold mb-2">
                🌱 Soil Type
              </label>

              <select
                name="soil_type"
                value={formData.soil_type}
                onChange={handleChange}
                className="w-full border border-gray-300 p-4 rounded-xl outline-none focus:ring-2 focus:ring-green-600"
              >

                <option value="low">
                  Low Fertility
                </option>

                <option value="medium">
                  Medium Fertility
                </option>

                <option value="high">
                  High Fertility
                </option>

              </select>

            </div>

            {/* -------------------------------- */}
            {/* Month */}
            {/* -------------------------------- */}

            <div>

              <label className="block text-gray-700 font-semibold mb-2">
                📅 Month
              </label>

              <select
                name="month"
                value={formData.month}
                onChange={handleChange}
                className="w-full border border-gray-300 p-4 rounded-xl outline-none focus:ring-2 focus:ring-green-600"
              >

                {months.map((month) => (
                  <option
                    key={month.value}
                    value={month.value}
                  >
                    {month.name}
                  </option>
                ))}

              </select>

            </div>

            {/* -------------------------------- */}
            {/* Submit Button */}
            {/* -------------------------------- */}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-700 hover:bg-green-800 disabled:bg-gray-400 text-white py-4 rounded-xl font-semibold text-lg transition"
            >

              {loading
                ? "🔄 Finding Best Crop..."
                : "🌾 Recommend Crop"}

            </button>

          </form>

          {/* -------------------------------- */}
          {/* Result */}
          {/* -------------------------------- */}

          {result && (

            <div className="mt-8">

              {!result.success ? (

                <div className="bg-red-100 border border-red-300 text-red-700 p-4 rounded-xl">
                  ❌ {result.message}
                </div>

              ) : (

                <div className="bg-green-50 border border-green-200 rounded-2xl p-6">

                  {/* Recommended Crop */}

                  <div className="text-center mb-6">

                    <p className="text-gray-600">
                      🌾 Recommended Crop
                    </p>

                    <h2 className="text-4xl font-bold text-green-700 mt-2 capitalize">
                      {result.recommended_crop}
                    </h2>

                  </div>

                  {/* Details */}

                  <div className="grid md:grid-cols-2 gap-4">

                    <div className="bg-white rounded-xl p-4 shadow-sm">
                      <p className="text-gray-500">
                        🇮🇳 State
                      </p>

                      <p className="font-semibold text-lg">
                        {locationData.state}
                      </p>
                    </div>

                    <div className="bg-white rounded-xl p-4 shadow-sm">
                      <p className="text-gray-500">
                        📍 District
                      </p>

                      <p className="font-semibold text-lg">
                        {locationData.district}
                      </p>
                    </div>

                    <div className="bg-white rounded-xl p-4 shadow-sm">
                      <p className="text-gray-500">
                        🏘️ Sub-District
                      </p>

                      <p className="font-semibold text-lg">
                        {locationData.sub_district}
                      </p>
                    </div>

                    <div className="bg-white rounded-xl p-4 shadow-sm">
                      <p className="text-gray-500">
                        🌱 Soil Type
                      </p>

                      <p className="font-semibold text-lg capitalize">
                        {result.soil_type}
                      </p>
                    </div>

                    <div className="bg-white rounded-xl p-4 shadow-sm">
                      <p className="text-gray-500">
                        🌡️ Temperature
                      </p>

                      <p className="font-semibold text-lg">
                        {result.weather?.temperature} °C
                      </p>
                    </div>

                    <div className="bg-white rounded-xl p-4 shadow-sm">
                      <p className="text-gray-500">
                        💧 Humidity
                      </p>

                      <p className="font-semibold text-lg">
                        {result.weather?.humidity} %
                      </p>
                    </div>

                    <div className="bg-white rounded-xl p-4 shadow-sm md:col-span-2">
                      <p className="text-gray-500">
                        🌧️ Rainfall
                      </p>

                      <p className="font-semibold text-lg">
                        {result.weather?.rainfall} mm
                      </p>
                    </div>

                  </div>

                </div>

              )}

            </div>

          )}

        </div>

      </div>

    </div>
  );
}

export default CropRecommendation;