function Features() {
  return (
    <section className="min-h-screen py-20 bg-white">
      <div className="max-w-7xl mx-auto px-6">

        <h2 className="text-4xl font-bold text-center text-green-700 mb-12">
          🌾 Our Features
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          <div className="bg-green-50 p-6 rounded-xl shadow hover:shadow-lg transition">
            <h3 className="text-2xl font-bold mb-3">
              🌱 Crop Recommendation
            </h3>
            <p className="text-gray-600">
              AI recommends the best crop based on soil nutrients,
              rainfall, humidity, temperature and pH.
            </p>
          </div>

          <div className="bg-green-50 p-6 rounded-xl shadow hover:shadow-lg transition">
            <h3 className="text-2xl font-bold mb-3">
              🍃 Disease Detection
            </h3>
            <p className="text-gray-600">
              Upload crop leaf images to detect diseases and receive
              treatment suggestions.
            </p>
          </div>

          <div className="bg-green-50 p-6 rounded-xl shadow hover:shadow-lg transition">
            <h3 className="text-2xl font-bold mb-3">
              ☁️ Weather Forecast
            </h3>
            <p className="text-gray-600">
              Get real-time weather updates and forecasts to make better
              farming decisions.
            </p>
          </div>

          <div className="bg-green-50 p-6 rounded-xl shadow hover:shadow-lg transition">
            <h3 className="text-2xl font-bold mb-3">
              📈 Mandi Rates
            </h3>
            <p className="text-gray-600">
              View the latest crop prices from various mandis across India.
            </p>
          </div>

          <div className="bg-green-50 p-6 rounded-xl shadow hover:shadow-lg transition">
            <h3 className="text-2xl font-bold mb-3">
              🤖 AI Chatbot
            </h3>
            <p className="text-gray-600">
              Ask agriculture-related questions in Hindi or English and get
              AI-powered guidance.
            </p>
          </div>

          <div className="bg-green-50 p-6 rounded-xl shadow hover:shadow-lg transition">
            <h3 className="text-2xl font-bold mb-3">
              🌾 Farmer Advisory
            </h3>
            <p className="text-gray-600">
              Receive personalized farming advice based on current weather
              conditions.
            </p>
          </div>

        </div>

      </div>
    </section>
  );
}

export default Features;