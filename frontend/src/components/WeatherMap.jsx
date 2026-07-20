import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect } from "react";
import { useMap } from "react-leaflet";
import { useState} from "react";
// Fix marker icons
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});
function ChangeMapView({ lat, lon }) {
  const map = useMap();

  useEffect(() => {
    if (lat && lon) {
      map.setView([lat, lon], 15, {
        animate: true,
      });
    }
  }, [lat, lon, map]);

  return null;
}
export default function WeatherMap({
  lat,
  lon,
  city,
  weather,
  farmLocation,
}) {
    const [satelliteView, setSatelliteView] = useState(false);
  if (!lat || !lon) return null;

  return (
    <div className="relative mt-10 bg-white rounded-3xl shadow-xl p-4">
      <h2 className="text-3xl font-bold text-green-700 mb-4">
        🗺 Live Weather Map
      </h2>

      <MapContainer
        center={[lat, lon]}
        zoom={15}
        style={{
          height: "500px",
          width: "100%",
          borderRadius: "20px",
        }}
      >
        <button
  onClick={() => setSatelliteView(!satelliteView)}
  className="absolute top-4 right-4 z-[1000] bg-white px-4 py-2 rounded-xl shadow-lg font-semibold"
>
  {satelliteView ? "🗺 Street" : "🛰 Satellite"}
</button>
         <ChangeMapView lat={lat} lon={lon} />
        <TileLayer
 
  attribution="&copy; OpenStreetMap"
  url={
    satelliteView
      ? "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
      : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
  }
/>
  {farmLocation && (
  <Marker position={[farmLocation.lat, farmLocation.lon]}>
    <Popup>
      <div className="text-center">
        <h3 className="font-bold">🌾 My Farm</h3>
        <p>Your saved farm location</p>
      </div>
    </Popup>
  </Marker>
)}
        <Marker position={[lat, lon]}>
          <Popup>
  <div className="text-center">
    <h3 className="text-lg font-bold">📍 {city}</h3>

    <p>🌡 Temperature: {weather?.temperature}°C</p>

    <p>☁ Condition: {weather?.condition}</p>

    <p>💧 Humidity: {weather?.humidity}%</p>

    <p>🌬 Wind: {weather?.wind_speed} km/h</p>

    <p>🌾 AgriSmart AI</p>
  </div>

</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}