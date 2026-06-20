import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <>
      <Navbar />

      {/* Hero Section */}
      <section className="min-h-screen bg-gradient-to-br from-green-900 via-green-700 to-green-500 text-white flex flex-col justify-center items-center px-6">
        <h1 className="text-6xl md:text-7xl font-bold text-center">
          🌾 AgriSmart AI
        </h1>

        <p className="mt-6 text-xl text-center max-w-3xl">
          Empowering Indian Farmers with AI-powered Crop Recommendation,
          Disease Detection, Weather Forecasting and Mandi Intelligence.
        </p>

        <button
          onClick={() => navigate("/dashboard")}
          className="mt-8 px-8 py-4 bg-white text-green-700 rounded-xl font-bold hover:scale-105 transition duration-300"
        >
          Get Started
        </button>
      </section>

      {/* Features Section */}
      <section className="bg-white py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-green-700 mb-12">
            Our Features
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-green-50 p-8 rounded-2xl shadow-md hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3">
                🌱 Crop Recommendation
              </h3>
              <p className="text-gray-600">
                AI suggests the best crop based on soil nutrients,
                temperature, rainfall and pH level.
              </p>
            </div>

            <div className="bg-green-50 p-8 rounded-2xl shadow-md hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3">
                🍃 Disease Detection
              </h3>
              <p className="text-gray-600">
                Upload crop leaf images and instantly identify diseases
                with AI-powered analysis.
              </p>
            </div>

            <div className="bg-green-50 p-8 rounded-2xl shadow-md hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3">
                ☁️ Weather Forecast
              </h3>
              <p className="text-gray-600">
                Get real-time weather information and 7-day forecasts
                to plan farming activities.
              </p>
            </div>

            <div className="bg-green-50 p-8 rounded-2xl shadow-md hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3">
                📈 Mandi Rates
              </h3>
              <p className="text-gray-600">
                Check latest mandi prices and market trends for crops
                across different regions.
              </p>
            </div>

            <div className="bg-green-50 p-8 rounded-2xl shadow-md hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3">
                🤖 AI Chatbot
              </h3>
              <p className="text-gray-600">
                Ask farming questions in Hindi or English and receive
                intelligent agricultural guidance.
              </p>
            </div>

            <div className="bg-green-50 p-8 rounded-2xl shadow-md hover:shadow-xl transition">
              <h3 className="text-2xl font-bold mb-3">
                💰 Profit Calculator
              </h3>
              <p className="text-gray-600">
                Estimate farming expenses, revenue and expected profit
                before cultivation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-green-900 text-white py-8">
        <div className="max-w-7xl mx-auto text-center">
          <h3 className="text-2xl font-bold">🌾 AgriSmart AI</h3>

          <p className="mt-3 text-gray-300">
            Empowering Farmers Through Technology
          </p>

          <p className="mt-2 text-sm text-gray-400">
            © 2026 AgriSmart AI. All Rights Reserved.
          </p>
        </div>
      </footer>
    </>
  );
}

export default Home;