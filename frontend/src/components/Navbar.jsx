import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full bg-white shadow-md z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

        <Link to="/" className="text-2xl font-bold text-green-700">
          🌾 AgriSmart AI
        </Link>

        <div className="space-x-6 font-medium">

          <Link to="/" className="hover:text-green-700">
            Home
          </Link>

          <Link to="/features" className="hover:text-green-700">
            Features
          </Link>

          <Link to="/about" className="hover:text-green-700">
            About
          </Link>

          <Link to="/contact" className="hover:text-green-700">
            Contact
          </Link>

        </div>

      </div>
    </nav>
  );
}

export default Navbar;