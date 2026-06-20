function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full bg-white shadow-md z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

        <h1 className="text-2xl font-bold text-green-700">
          🌾 AgriSmart AI
        </h1>

        <div className="space-x-6 font-medium">
          <a href="#" className="hover:text-green-700">
            Home
          </a>

          <a href="#" className="hover:text-green-700">
            Features
          </a>

          <a href="#" className="hover:text-green-700">
            About
          </a>

          <a href="#" className="hover:text-green-700">
            Contact
          </a>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;