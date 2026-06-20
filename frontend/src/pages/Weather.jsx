import { useState } from "react";
import api from "../services/api";

function Weather() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);

  const getWeather = async () => {
    try {
      const response = await api.get(`/weather/${city}`);
      setWeather(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow-lg">

        <h1 className="text-4xl font-bold text-green-700 mb-6">
          ☁️ Weather Forecast
        </h1>

        <input
          type="text"
          placeholder="Enter City Name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="w-full border p-3 rounded-lg mb-4"
        />

        <button
          onClick={getWeather}
          className="w-full bg-green-700 text-white py-3 rounded-lg"
        >
          Get Weather
        </button>

        {weather && (
          <div className="mt-6 bg-green-100 p-5 rounded-lg">
            <h2 className="text-2xl font-bold">
              {weather.city}
            </h2>

            <p>🌡 Temperature: {weather.temperature}°C</p>
            <p>💧 Humidity: {weather.humidity}%</p>
            <p>🌬 Wind Speed: {weather.wind_speed} km/h</p>
            <p>☁ Condition: {weather.condition}</p>
          </div>
        )}

      </div>
    </div>
  );
}

export default Weather;