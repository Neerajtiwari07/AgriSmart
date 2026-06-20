import { Link } from "react-router-dom";

function Dashboard() {
  const stats = [
    { title: "Crop Predictions", value: 120, icon: "🌱" },
    { title: "Disease Checks", value: 45, icon: "🍃" },
    { title: "Weather Searches", value: 89, icon: "☁️" },
    { title: "AI Questions", value: 210, icon: "🤖" },
  ];

  const actions = [
    {
      title: "Crop Recommendation",
      icon: "🌱",
      link: "/crop-recommendation",
    },
    {
      title: "Disease Detection",
      icon: "🍃",
      link: "/disease-detection",
    },
    {
      title: "Weather Forecast",
      icon: "☁️",
      link: "/weather",
    },
    {
      title: "Mandi Rates",
      icon: "📈",
      link: "/mandi-rates",
    },
    {
      title: "AI Chatbot",
      icon: "🤖",
      link: "/chatbot",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100 flex">

      {/* Sidebar */}
      <div className="w-64 bg-green-800 text-white p-6">

        <h1 className="text-3xl font-bold mb-8">
          🌾 AgriSmart AI
        </h1>

        <div className="space-y-4">

          <Link to="/dashboard" className="block hover:text-green-200">
            Dashboard
          </Link>

          <Link to="/crop-recommendation" className="block hover:text-green-200">
            Crop Recommendation
          </Link>

          <Link to="/disease-detection" className="block hover:text-green-200">
            Disease Detection
          </Link>

          <Link to="/weather" className="block hover:text-green-200">
            Weather Forecast
          </Link>

          <Link to="/mandi-rates" className="block hover:text-green-200">
            Mandi Rates
          </Link>

          <Link to="/chatbot" className="block hover:text-green-200">
            AI Chatbot
          </Link>

        </div>

      </div>

      {/* Main Content */}
      <div className="flex-1 p-8">

        <h1 className="text-4xl font-bold text-green-700 mb-8">
          👨‍🌾 Farmer Dashboard
        </h1>

        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-10">

          {stats.map((item, index) => (
            <div
              key={index}
              className="bg-white p-6 rounded-2xl shadow-md"
            >
              <div className="text-4xl">{item.icon}</div>

              <h2 className="mt-3 font-bold text-lg">
                {item.title}
              </h2>

              <p className="text-3xl text-green-700 font-bold mt-2">
                {item.value}
              </p>
            </div>
          ))}

        </div>

        {/* Quick Actions */}
        <h2 className="text-2xl font-bold mb-6">
          ⚡ Quick Actions
        </h2>

        <div className="grid md:grid-cols-3 gap-6">

          {actions.map((item, index) => (
            <Link
              key={index}
              to={item.link}
              className="bg-white p-8 rounded-2xl shadow-md hover:shadow-xl transition"
            >
              <div className="text-5xl mb-4">
                {item.icon}
              </div>

              <h3 className="text-xl font-bold">
                {item.title}
              </h3>
            </Link>
          ))}

        </div>

      </div>

    </div>
  );
}

export default Dashboard;