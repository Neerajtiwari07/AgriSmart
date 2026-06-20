import { useState } from "react";
import api from "../services/api";

function DiseaseDetection() {
  const [image, setImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];

    if (file) {
      setSelectedFile(file);
      setImage(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleDetectDisease = async () => {
    if (!selectedFile) {
      alert("Please select an image first");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await api.post(
        "/detect-disease",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);

    } catch (error) {
      console.error("Error:", error);

      setResult({
        disease: "Error",
        confidence: "0%",
        treatment: "Failed to connect backend",
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <div className="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow-lg">

        <h1 className="text-4xl font-bold text-green-700 mb-6">
          🍃 Plant Disease Detection
        </h1>

        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="mb-6"
        />

        {image && (
          <img
            src={image}
            alt="Plant"
            className="w-full h-80 object-cover rounded-xl"
          />
        )}

        <button
          onClick={handleDetectDisease}
          className="mt-6 w-full bg-green-700 text-white py-3 rounded-lg hover:bg-green-800 transition"
        >
          Detect Disease
        </button>

        {result && (
          <div className="mt-6 bg-green-100 p-5 rounded-lg">

            <h2 className="text-2xl font-bold text-green-700">
              Disease: {result.disease}
            </h2>

            <p className="mt-3 text-lg">
              Confidence: {result.confidence}
            </p>

            <p className="mt-3">
              Treatment: {result.treatment}
            </p>

          </div>
        )}

      </div>

    </div>
  );
}

export default DiseaseDetection;