function Contact() {
  return (
    <section className="min-h-screen py-20 bg-green-50">
      <div className="max-w-4xl mx-auto px-6">

        <h2 className="text-4xl font-bold text-center text-green-700 mb-10">
          📞 Contact Us
        </h2>

        <form className="bg-white p-8 rounded-2xl shadow-lg">

          <input
            type="text"
            placeholder="Your Name"
            className="w-full border p-3 rounded-lg mb-4"
          />

          <input
            type="email"
            placeholder="Your Email"
            className="w-full border p-3 rounded-lg mb-4"
          />

          <textarea
            rows="5"
            placeholder="Your Message"
            className="w-full border p-3 rounded-lg mb-4"
          ></textarea>

          <button
            className="w-full bg-green-700 text-white py-3 rounded-lg hover:bg-green-800 transition"
          >
            Send Message
          </button>

        </form>

        <div className="text-center mt-10">

          <h3 className="text-2xl font-bold text-green-700">
            🌾 AgriSmart AI
          </h3>

          <p className="mt-3 text-gray-600">
            Email: support@agrismartai.com
          </p>

          <p className="text-gray-600">
            Phone: +91 98765 43210
          </p>

          <p className="text-gray-600">
            Lucknow, Uttar Pradesh, India
          </p>

        </div>

      </div>
    </section>
  );
}

export default Contact;