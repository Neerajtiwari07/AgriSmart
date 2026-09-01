import { useState } from "react";
import locations from "../data/locations";

function Location({ onLocationChange }) {
  const [state, setState] = useState("");
  const [district, setDistrict] = useState("");
  const [subDistrict, setSubDistrict] = useState("");

  // All states
  const states = Object.keys(locations);

  // Districts according to selected state
  const districts = state
    ? Object.keys(locations[state])
    : [];

  // Sub-districts according to selected district
  const subDistricts =
    state && district
      ? locations[state][district]
      : [];

  const handleStateChange = (e) => {
    const selectedState = e.target.value;

    setState(selectedState);
    setDistrict("");
    setSubDistrict("");

    if (onLocationChange) {
      onLocationChange({
        state: selectedState,
        district: "",
        sub_district: "",
      });
    }
  };

  const handleDistrictChange = (e) => {
    const selectedDistrict = e.target.value;

    setDistrict(selectedDistrict);
    setSubDistrict("");

    if (onLocationChange) {
      onLocationChange({
        state,
        district: selectedDistrict,
        sub_district: "",
      });
    }
  };

  const handleSubDistrictChange = (e) => {
    const selectedSubDistrict = e.target.value;

    setSubDistrict(selectedSubDistrict);

    if (onLocationChange) {
      onLocationChange({
        state,
        district,
        sub_district: selectedSubDistrict,
      });
    }
  };

  return (
    <div className="space-y-5">

      {/* State */}
      <div>
        <label className="block text-gray-700 font-semibold mb-2">
          🇮🇳 State
        </label>

        <select
          value={state}
          onChange={handleStateChange}
          className="w-full border border-gray-300 p-4 rounded-xl outline-none focus:ring-2 focus:ring-green-600"
        >
          <option value="">
            Select State
          </option>

          {states.map((stateName) => (
            <option
              key={stateName}
              value={stateName}
            >
              {stateName}
            </option>
          ))}
        </select>
      </div>

      {/* District */}
      <div>
        <label className="block text-gray-700 font-semibold mb-2">
          📍 District
        </label>

        <select
          value={district}
          onChange={handleDistrictChange}
          disabled={!state}
          className="w-full border border-gray-300 p-4 rounded-xl outline-none focus:ring-2 focus:ring-green-600 disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">
            {state
              ? "Select District"
              : "First Select State"}
          </option>

          {districts.map((districtName) => (
            <option
              key={districtName}
              value={districtName}
            >
              {districtName}
            </option>
          ))}
        </select>
      </div>

      {/* Sub-District */}
      <div>
        <label className="block text-gray-700 font-semibold mb-2">
          🏘️ Sub-District / Tehsil
        </label>

        <select
          value={subDistrict}
          onChange={handleSubDistrictChange}
          disabled={!district}
          className="w-full border border-gray-300 p-4 rounded-xl outline-none focus:ring-2 focus:ring-green-600 disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          <option value="">
            {district
              ? "Select Sub-District"
              : "First Select District"}
          </option>

          {subDistricts.map((subDistrictName) => (
            <option
              key={subDistrictName}
              value={subDistrictName}
            >
              {subDistrictName}
            </option>
          ))}
        </select>
      </div>

    </div>
  );
}

export default Location;