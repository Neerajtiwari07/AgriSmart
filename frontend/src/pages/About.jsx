import Navbar from "../components/Navbar";

function About() {
  return (
    <>
      <Navbar />

      <section className="min-h-screen py-24 bg-green-50">
        <div className="max-w-6xl mx-auto px-6">

          <h1 className="text-5xl font-bold text-center text-green-700 mb-8">
            🌾 About AgriSmart AI
          </h1>

          <p className="text-lg text-gray-700 text-center leading-8 max-w-4xl mx-auto">
            AgriSmart AI is a smart farming assistant designed to support
            farmers with modern agricultural guidance. Our goal is to help
            farmers make better decisions, improve crop production, reduce
            losses, and increase their income through easy-to-use digital
            solutions.
          </p>

          <div className="grid md:grid-cols-3 gap-8 mt-16">

            <div className="bg-white p-8 rounded-2xl shadow-lg">
              <div className="text-5xl mb-4 text-center">🌱</div>

              <h2 className="text-2xl font-bold text-center text-green-700">
                Our Mission
              </h2>

              <p className="mt-4 text-gray-600 text-center">
                To empower every farmer with reliable information, helping
                them grow healthy crops, reduce farming risks, and improve
                productivity.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg">
              <div className="text-5xl mb-4 text-center">🌍</div>

              <h2 className="text-2xl font-bold text-center text-green-700">
                Our Vision
              </h2>

              <p className="mt-4 text-gray-600 text-center">
                To build a future where every farmer can easily access
                weather updates, crop advice, disease detection, and market
                information from one platform.
              </p>
            </div>

            <div className="bg-white p-8 rounded-2xl shadow-lg">
              <div className="text-5xl mb-4 text-center">❤️</div>

              <h2 className="text-2xl font-bold text-center text-green-700">
                Why AgriSmart AI?
              </h2>

              <p className="mt-4 text-gray-600 text-center">
                AgriSmart AI provides crop recommendations, weather updates,
                disease detection, mandi prices, and farming guidance to
                help farmers make informed decisions throughout the farming
                season.
              </p>
            </div>

          </div>

        </div>
      </section>
    </>
  );
}

export default About;