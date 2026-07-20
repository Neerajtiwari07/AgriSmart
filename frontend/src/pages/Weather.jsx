import { useState, useEffect } from "react";
import WeatherMap from "../components/WeatherMap";
import api from "../services/api";

 
// Local Backend//

function Weather() {

  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [advisory, setAdvisory] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);
  const [farmLocation, setFarmLocation] = useState(null);
  const response = await api.get("/weather-location", {
  params: {
    lat,
    lon,
  },
});
  // -----------------------------
  // Get Current Location Weather
  // -----------------------------
  const getCurrentLocation = () => {

    if (!navigator.geolocation) {
      alert("Geolocation is not supported.");
      return;
    }

    navigator.geolocation.getCurrentPosition(

      async (position) => {

        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        setLat(lat);
        setLon(lon);

        try {

          setLoading(true);
          setError("");

          const response = await api.get("/weather-location", {
  params: {
    lat,
    lon,
  },
});

          setWeather(response.data.weather);
          setForecast(response.data.forecast);
          setAdvisory(response.data.advisory);

          // Optional: show current location
          setCity(response.data.city);

        } catch (err) {

          console.log(err);
          setError("Unable to fetch current location weather.");

        } finally {

          setLoading(false);

        }

      },

      () => {

        alert("Location permission denied.");

      }

    );

  };
 
  // -----------------------------
  // Press Enter to Search
  // -----------------------------
  useEffect(() => {
  getCurrentLocation();

  const interval = setInterval(() => {
    getCurrentLocation();
  }, 60000); // 60 seconds

  return () => clearInterval(interval);
}, []);
return (
<div className="min-h-screen bg-gradient-to-br from-blue-100 via-green-100 to-green-200">

<div className="max-w-7xl mx-auto px-6 py-10">

{/* Heading */}

<h1 className="text-5xl font-bold text-center text-green-700">
🌾 AgriSmart AI Weather
</h1>

<p className="text-center text-gray-600 mt-3 text-lg">
Real-Time Weather • Live Location • AI Farmer Advisory
</p>

<div className="bg-white rounded-3xl shadow-2xl p-8 mt-10">

  <div className="flex flex-col md:flex-row items-center justify-between gap-6">

    <div>
      <h2 className="text-3xl font-bold text-green-700">
        📍 Current Location
      </h2>

      <p className="text-xl text-gray-700 mt-2">
        {city || "Detecting location..."}
      </p>

      <p className="text-green-600 font-semibold mt-2">
        🟢 Live Weather Updates
      </p>
    </div>

    <button
      onClick={getCurrentLocation}
      className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-semibold shadow-lg transition"
    >
      🔄 Refresh Weather
    </button>

  </div>

{/* Loading */}

{loading && (

<div className="text-center mt-8">

<div className="animate-spin rounded-full h-16 w-16 border-4 border-green-600 border-t-transparent mx-auto"></div>

<p className="mt-4 font-semibold text-lg">
Loading Weather...
</p>

</div>

)}

{/* Error */}

{error && (

<div className="bg-red-100 text-red-700 mt-6 rounded-xl p-4 text-center font-semibold">

{error}

</div>

)}

{/* Current Weather */}

{weather && (

<div className="mt-10">

<div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

{/* Main Card */}

<div className="bg-gradient-to-r from-green-500 to-green-700 text-white rounded-3xl shadow-lg p-6">

<h2 className="text-2xl font-bold">

📍 {city}

</h2>

<p className="text-6xl font-bold mt-4">

{weather.temperature}°C

</p>

<p className="mt-4 text-xl">

☁ {weather.condition}

</p>

<p className="text-blue-600 font-semibold">
    🌧 Rain Chance: {weather?.rain_probability}%
</p>

</div>


{/* Humidity */}

<div className="bg-blue-100 rounded-3xl shadow-lg p-6">

<div className="text-5xl">
💧
</div>

<h3 className="text-xl font-bold mt-4">

Humidity

</h3>

<p className="text-5xl text-blue-700 font-bold mt-5">

{weather.humidity}%

</p>

</div>

{/* Wind */}

<div className="bg-yellow-100 rounded-3xl shadow-lg p-6">

<div className="text-5xl">
🌬
</div>

<h3 className="text-xl font-bold mt-4">

Wind Speed

</h3>

<p className="text-5xl text-yellow-700 font-bold mt-5">

{weather.wind_speed}

</p>

<p className="mt-2">

km/h

</p>

</div>


{/* Condition */}

<div className="bg-purple-100 rounded-3xl shadow-lg p-6">

<div className="text-5xl">
🌤
</div>

<h3 className="text-xl font-bold mt-4">

Condition

</h3>

<p className="text-2xl font-semibold mt-6">

{weather.condition}

</p>

</div>

</div>
</div>

)}

      {/* Farmer Advisory */}

      {advisory && (

        <div className="mt-10">

          <div className="bg-gradient-to-r from-yellow-100 to-green-100 rounded-3xl shadow-xl p-6">

            <h2 className="text-3xl font-bold text-green-700">

              🌾 AI Farmer Advisory

            </h2>

            <p className="mt-5 text-lg leading-8 text-gray-700">

              {advisory}

            </p>

          </div>

        </div>

      )}

      {/* 7 Days Forecast */}

      {forecast.length > 0 && (

      

        <div className="mt-12">

          <h2 className="text-3xl font-bold text-green-700 mb-8">

            📅 7 Days Weather Forecast

          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-7 gap-6">

            {forecast.map((day, index) => (
               
            

              <div
                key={index}
                className="bg-white rounded-2xl shadow-lg p-5 hover:shadow-2xl hover:-translate-y-2 transition duration-300"
              >

                <h3 className="text-lg font-bold text-center text-green-700">

                  {new Date(day.date).toLocaleDateString("en-IN", {
                    weekday: "short",
                  })}

                </h3>

                <p className="text-center text-gray-500 text-sm">

                  {day.date}

                </p>

                <div className="text-center text-5xl mt-5">

                  {day.condition.includes("Rain")
                    ? "🌧"
                    : day.condition.includes("Cloud")
                    ? "☁"
                    : day.condition.includes("Snow")
                    ? "❄"
                    : day.condition.includes("Thunder")
                    ? "⛈"
                    : "☀"}

                </div>

                <p className="text-center mt-4 font-semibold text-gray-700">

                  {day.condition}

                </p>

                <div className="mt-6 space-y-2">

  <p className="text-red-600 font-bold">
    🔺 Max : {day.max_temp}°C
  </p>

  <p className="text-blue-600 font-bold">
    🔻 Min : {day.min_temp}°C
  </p>

  {/* 👇 Is line ko replace karna hai */}
  <p
    className={`font-bold mt-2 ${
      day.rain_probability >= 70
        ? "text-red-600"
        : day.rain_probability >= 40
        ? "text-yellow-600"
        : "text-green-600"
    }`}
  >
    🌧 Rain Chance: {day.rain_probability}%
  </p>


                </div>

              </div>

            ))}

          </div>
    {lat && lon && (
  <WeatherMap
    lat={lat}
    lon={lon}
    city={city}
    weather={weather}
    farmLocation={farmLocation}
    setFarmLocation={setFarmLocation}
  />
)}
        </div>

      )}

      {/* Footer */}

      <div className="mt-16 border-t pt-6 text-center text-gray-500">

        <p className="text-lg font-semibold">

          🌾 Powered by AgriSmart AI

        </p>

        <p className="text-sm mt-2">
          © 2026 AgriSmart AI. All rights reserved. 


        </p>

      </div>

    </div>
  
  </div>

</div>
);

}

export default Weather;