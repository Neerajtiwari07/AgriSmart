import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import CropRecommendation from "./pages/CropRecommendation";
import DiseaseDetection from "./pages/DiseaseDetection";
import Weather from "./pages/Weather";
import MandiRates from "./pages/MandiRates";
import Chatbot from "./pages/Chatbot";
import ProfitCalculator from "./pages/ProfitCalculator";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />

        <Route
          path="/crop-recommendation"
          element={<CropRecommendation />}
        />

        <Route
          path="/disease-detection"
          element={<DiseaseDetection />}
        />

        <Route
          path="/weather"
          element={<Weather />}
        />

        <Route
          path="/mandi-rates"
          element={<MandiRates />}
        />

        <Route
          path="/chatbot"
          element={<Chatbot />}
        />

        <Route
          path="/profit-calculator"
          element={<ProfitCalculator />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;