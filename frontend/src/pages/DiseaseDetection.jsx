import { useRef, useState } from "react";
import api from "../services/api";

function DiseaseDetection() {
  const [image, setImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);

  const [language, setLanguage] = useState("en");

  const fileInputRef = useRef(null);

  // ============================================================
  // TRANSLATIONS
  // ============================================================

  const translations = {
    en: {
      language: "Language",
      english: "English",
      hindi: "हिंदी",
      hinglish: "Hinglish",

      title: "Plant Disease Detection",

      subtitle:
        "Upload a clear leaf image and let our AI model analyze it for possible plant diseases.",

      imageReady: "Image Ready",
      selectedLeaf: "Selected Leaf Image",
      remove: "Remove",

      uploadLeaf: "Upload Leaf Image",
      dragDrop: "Drag & drop your image here",
      or: "OR",
      browse: "Browse Image",

      fileInfo:
        "PNG, JPG, JPEG • Clear leaf images recommended",

      readyAnalysis: "Ready for AI analysis",

      analyze: "Analyze with AI",
      analyzing: "AI is analyzing...",

      imageQuality: "Image Quality",
      betterImage: "Please upload a better image",

      recommendation: "Recommendation",

      aiUncertain: "AI Uncertain",
      unableIdentify: "Unable to confidently identify",

      modelConfidence: "Model Confidence",

      topPredictions: "Top AI Predictions",

      predictionDescription:
        "These are the classes the model considered most likely.",

      reviewRequired: "AI Review Required",

      mismatchTitle:
        "Crop and disease predictions do not match",

      mismatchMessage:
        "The crop and disease predictions do not match. The AI result requires additional review.",

      safetyCheck: "Safety Check",

      safetyMessage:
        "The system detected a mismatch between the crop identified by the crop model and the crop associated with the disease prediction. Please upload a clearer image or manually verify the plant before using the result.",

      predictionComparison:
        "AI Prediction Comparison",

      cropModel: "Crop Model",
      diseaseModel: "Disease Model",

      confidence: "Confidence",

      diseaseCrop:
        "Crop Associated With Disease Prediction",

      confirmedPrediction: "AI Prediction",

      crop: "Crop",

      classification: "Model Classification",

      symptoms: "Symptoms",

      management: "Management",

      prevention: "Prevention",

      source: "Information Source",

      error: "Error",

      detectionFailed:
        "Disease detection failed",

      errorMessage:
        "Something went wrong while analyzing the image.",

      unknown: "Unknown",

      noSymptoms:
        "No symptom information available.",

      noManagement:
        "No management information available.",

      noPrevention:
        "No prevention information available.",

      clearLeaf:
        "Please upload a clear close-up image of a single affected leaf.",

      reviewRecommendation:
        "Upload a clear close-up image showing a single plant leaf.",

      mismatchRecommendation:
        "Upload a clear close-up image containing one clearly visible leaf. If possible, verify the crop manually before analyzing again.",

      topDiseasePredictions:
        "Top Disease Predictions",
    },

    hi: {
      language: "भाषा",
      english: "English",
      hindi: "हिंदी",
      hinglish: "Hinglish",

      title: "पौधों की बीमारी पहचान",

      subtitle:
        "पत्ती की साफ तस्वीर अपलोड करें और हमारा AI मॉडल संभावित पौधों की बीमारियों का विश्लेषण करेगा।",

      imageReady: "तस्वीर तैयार है",
      selectedLeaf: "चयनित पत्ती की तस्वीर",
      remove: "हटाएं",

      uploadLeaf: "पत्ती की तस्वीर अपलोड करें",
      dragDrop: "अपनी तस्वीर यहां Drag & Drop करें",
      or: "या",
      browse: "तस्वीर चुनें",

      fileInfo:
        "PNG, JPG, JPEG • साफ पत्ती की तस्वीर बेहतर रहेगी",

      readyAnalysis: "AI विश्लेषण के लिए तैयार",

      analyze: "AI से विश्लेषण करें",
      analyzing: "AI विश्लेषण कर रहा है...",

      imageQuality: "तस्वीर की गुणवत्ता",
      betterImage: "कृपया बेहतर तस्वीर अपलोड करें",

      recommendation: "सुझाव",

      aiUncertain: "AI निश्चित नहीं है",
      unableIdentify:
        "AI बीमारी की पहचान निश्चित रूप से नहीं कर पाया",

      modelConfidence: "मॉडल का विश्वास स्तर",

      topPredictions: "AI की प्रमुख भविष्यवाणियां",

      predictionDescription:
        "ये वे वर्ग हैं जिन्हें मॉडल ने सबसे संभावित माना है।",

      reviewRequired: "AI समीक्षा आवश्यक है",

      mismatchTitle:
        "फसल और बीमारी की पहचान मेल नहीं खा रही है",

      mismatchMessage:
        "फसल और बीमारी की भविष्यवाणी आपस में मेल नहीं खा रही है। AI परिणाम की अतिरिक्त समीक्षा आवश्यक है।",

      safetyCheck: "सुरक्षा जांच",

      safetyMessage:
        "सिस्टम ने पाया कि Crop Model द्वारा पहचानी गई फसल और Disease Model से मिली बीमारी की फसल अलग है। कृपया अधिक साफ तस्वीर अपलोड करें या पौधे की फसल की पहचान स्वयं सत्यापित करें।",

      predictionComparison:
        "AI भविष्यवाणियों की तुलना",

      cropModel: "फसल मॉडल",
      diseaseModel: "बीमारी मॉडल",

      confidence: "विश्वास स्तर",

      diseaseCrop:
        "बीमारी की भविष्यवाणी से जुड़ी फसल",

      confirmedPrediction: "AI भविष्यवाणी",

      crop: "फसल",

      classification: "मॉडल वर्गीकरण",

      symptoms: "लक्षण",

      management: "प्रबंधन",

      prevention: "बचाव",

      source: "जानकारी का स्रोत",

      error: "त्रुटि",

      detectionFailed:
        "बीमारी की पहचान विफल हुई",

      errorMessage:
        "तस्वीर का विश्लेषण करते समय समस्या हुई।",

      unknown: "अज्ञात",

      noSymptoms:
        "लक्षण की जानकारी उपलब्ध नहीं है।",

      noManagement:
        "प्रबंधन की जानकारी उपलब्ध नहीं है।",

      noPrevention:
        "बचाव की जानकारी उपलब्ध नहीं है।",

      clearLeaf:
        "कृपया प्रभावित एक पत्ती की साफ और नजदीक से ली गई तस्वीर अपलोड करें।",

      reviewRecommendation:
        "एक साफ और नजदीक से ली गई पत्ती की तस्वीर अपलोड करें।",

      mismatchRecommendation:
        "एक ऐसी साफ तस्वीर अपलोड करें जिसमें एक पत्ती स्पष्ट रूप से दिखाई दे। संभव हो तो दोबारा विश्लेषण से पहले फसल की पहचान स्वयं सत्यापित करें।",

      topDiseasePredictions:
        "बीमारी की प्रमुख भविष्यवाणियां",
    },

    hinglish: {
      language: "Language",
      english: "English",
      hindi: "हिंदी",
      hinglish: "Hinglish",

      title: "Plant Disease Detection",

      subtitle:
        "Ek clear leaf image upload karo aur AI model possible plant disease ko analyze karega.",

      imageReady: "Image Ready",
      selectedLeaf: "Selected Leaf Image",
      remove: "Remove",

      uploadLeaf: "Leaf Image Upload Karo",
      dragDrop: "Apni image yahan Drag & Drop karo",
      or: "YA",
      browse: "Image Choose Karo",

      fileInfo:
        "PNG, JPG, JPEG • Clear leaf image recommended hai",

      readyAnalysis: "AI analysis ke liye ready",

      analyze: "AI Se Analyze Karo",
      analyzing: "AI analyze kar raha hai...",

      imageQuality: "Image Quality",
      betterImage: "Please ek better image upload karo",

      recommendation: "Recommendation",

      aiUncertain: "AI Uncertain",
      unableIdentify:
        "AI confidently disease identify nahi kar paya",

      modelConfidence: "Model Confidence",

      topPredictions: "Top AI Predictions",

      predictionDescription:
        "Ye classes hain jinhe model ne sabse likely maana hai.",

      reviewRequired: "AI Review Required",

      mismatchTitle:
        "Crop aur disease prediction match nahi kar rahe",

      mismatchMessage:
        "Crop aur disease prediction match nahi kar rahe. AI result ko additional review ki zarurat hai.",

      safetyCheck: "Safety Check",

      safetyMessage:
        "System ne detect kiya ki Crop Model ki prediction aur Disease Model se associated crop alag hain. Please clearer image upload karo ya plant ko manually verify karo.",

      predictionComparison:
        "AI Prediction Comparison",

      cropModel: "Crop Model",
      diseaseModel: "Disease Model",

      confidence: "Confidence",

      diseaseCrop:
        "Disease Prediction se Associated Crop",

      confirmedPrediction: "AI Prediction",

      crop: "Crop",

      classification: "Model Classification",

      symptoms: "Symptoms",

      management: "Management",

      prevention: "Prevention",

      source: "Information Source",

      error: "Error",

      detectionFailed:
        "Disease detection failed",

      errorMessage:
        "Image analyze karte time kuch problem hui.",

      unknown: "Unknown",

      noSymptoms:
        "Symptoms ki information available nahi hai.",

      noManagement:
        "Management information available nahi hai.",

      noPrevention:
        "Prevention information available nahi hai.",

      clearLeaf:
        "Ek clear close-up image upload karo jisme ek affected leaf clearly visible ho.",

      reviewRecommendation:
        "Ek clear close-up image upload karo jisme single plant leaf clearly visible ho.",

      mismatchRecommendation:
        "Ek clear image upload karo jisme ek leaf clearly visible ho. Possible ho to dobara analyze karne se pehle crop manually verify karo.",

      topDiseasePredictions:
        "Top Disease Predictions",
    },
  };

  const t = translations[language];

  // ============================================================
  // HANDLE FILE
  // ============================================================

  const handleFile = (file) => {
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please select a valid image file.");
      return;
    }

    setSelectedFile(file);
    setImage(URL.createObjectURL(file));
    setResult(null);
  };

  // ============================================================
  // IMAGE CHANGE
  // ============================================================

  const handleImageChange = (e) => {
    handleFile(e.target.files[0]);
  };

  // ============================================================
  // DRAG & DROP
  // ============================================================

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    handleFile(e.dataTransfer.files[0]);
  };

  // ============================================================
  // REMOVE IMAGE
  // ============================================================

  const handleRemoveImage = () => {
    setSelectedFile(null);
    setImage(null);
    setResult(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // ============================================================
  // DISEASE DETECTION
  // ============================================================

  const handleDetectDisease = async () => {
    if (!selectedFile) {
      alert(
        "Please upload a plant leaf image first."
      );
      return;
    }

    const formData = new FormData();

formData.append(
  "file",
  selectedFile
);

formData.append(
  "language",
  language
);

    setLoading(true);
    setResult(null);

    try {
      const response = await api.post(
        "/detect-disease",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      console.log(
        "Disease API Response:",
        response.data
      );

      setResult(response.data);
    } catch (error) {
      console.error(
        "Disease Detection Error:",
        error
      );

      setResult({
        success: false,
        status: "error",
        disease: "Error",
        confidence: "0%",
        disease_name:
          "Detection Failed",
        symptoms: "",
        management: "",
        prevention: "",
        source: "",
        error:
          "Unable to connect with the disease detection service.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-green-50 px-4 py-8 md:px-8">
      <div className="max-w-5xl mx-auto">

        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <div className="text-center mb-8">

          {/* Language Selector */}

          <div className="flex justify-end mb-5">

            <div className="flex items-center gap-2 bg-white border border-slate-200 shadow-sm rounded-xl px-3 py-2">

              <span className="text-lg">
                🌐
              </span>

              <label
                htmlFor="language"
                className="text-sm font-semibold text-slate-600"
              >
                {t.language}
              </label>

              <select
                id="language"
                value={language}
                onChange={(e) =>
                  setLanguage(
                    e.target.value
                  )
                }
                className="bg-transparent outline-none text-sm font-semibold text-slate-800 cursor-pointer"
              >
                <option value="en">
                  🇬🇧 {t.english}
                </option>

                <option value="hi">
                  🇮🇳 {t.hindi}
                </option>

                <option value="hinglish">
                  🇮🇳 {t.hinglish}
                </option>
              </select>

            </div>

          </div>


          {/* Logo */}

          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white shadow-lg border border-green-100 mb-4">

            <span className="text-4xl">
              🌿
            </span>

          </div>


          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900">
            {t.title}
          </h1>


          <p className="mt-3 text-slate-500 max-w-2xl mx-auto text-base md:text-lg">
            {t.subtitle}
          </p>

        </div>


        {/* ================================================= */}
        {/* UPLOAD CARD */}
        {/* ================================================= */}

        <div className="bg-white/80 backdrop-blur-xl border border-white rounded-3xl shadow-2xl p-5 md:p-7">

          {!image ? (

            <div
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragging(true);
              }}

              onDragLeave={() =>
                setIsDragging(false)
              }

              onDrop={handleDrop}

              onClick={() =>
                fileInputRef.current?.click()
              }

              className={`
                relative overflow-hidden
                cursor-pointer
                rounded-3xl
                border-2 border-dashed
                transition-all duration-300
                ${
                  isDragging
                    ? "border-emerald-500 bg-emerald-50 scale-[1.01]"
                    : "border-slate-200 bg-slate-50/70 hover:border-emerald-400 hover:bg-emerald-50/50"
                }
              `}
            >

              <div className="absolute -top-16 -right-16 w-40 h-40 rounded-full bg-emerald-100/50 blur-2xl" />

              <div className="absolute -bottom-16 -left-16 w-40 h-40 rounded-full bg-green-100/50 blur-2xl" />


              <div className="relative flex flex-col items-center justify-center text-center px-6 py-12 md:py-16">

                <div className="w-20 h-20 rounded-2xl bg-white shadow-lg border border-emerald-100 flex items-center justify-center mb-5">

                  <svg
                    className="w-10 h-10 text-emerald-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="1.7"
                      d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5"
                    />

                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="1.7"
                      d="M5 15v3a2 2 0 002 2h10a2 2 0 002-2v-3"
                    />
                  </svg>

                </div>


                <h2 className="text-2xl font-bold text-slate-800">
                  {t.uploadLeaf}
                </h2>

                <p className="mt-2 text-slate-500">
                  {t.dragDrop}
                </p>


                <div className="flex items-center gap-3 my-4">

                  <span className="h-px w-12 bg-slate-200" />

                  <span className="text-xs font-medium text-slate-400">
                    {t.or}
                  </span>

                  <span className="h-px w-12 bg-slate-200" />

                </div>


                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}

                  className="
                    inline-flex items-center gap-2
                    px-7 py-3
                    rounded-xl
                    bg-emerald-600
                    hover:bg-emerald-700
                    text-white
                    font-semibold
                    shadow-lg shadow-emerald-200
                    hover:-translate-y-0.5
                    transition-all
                  "
                >
                  <span>
                    📁
                  </span>

                  {t.browse}
                </button>


                <p className="mt-5 text-xs text-slate-400">
                  {t.fileInfo}
                </p>


                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                />

              </div>

            </div>

          ) : (

            /* ================================================= */
            /* IMAGE PREVIEW */
            /* ================================================= */

            <div>

              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-5">

                <div>

                  <p className="text-xs uppercase tracking-wider font-semibold text-emerald-600">
                    {t.imageReady}
                  </p>

                  <h2 className="text-xl font-bold text-slate-800 mt-1">
                    {t.selectedLeaf}
                  </h2>

                  <p className="text-sm text-slate-400 mt-1 break-all">
                    {selectedFile?.name}
                  </p>

                </div>


                <button
                  onClick={handleRemoveImage}
                  className="
                    self-start sm:self-auto
                    px-4 py-2
                    rounded-xl
                    bg-red-50
                    text-red-600
                    hover:bg-red-100
                    font-semibold
                    transition
                  "
                >
                  ✕ {t.remove}
                </button>

              </div>


              <div className="relative rounded-2xl overflow-hidden bg-slate-100 border border-slate-200">

                <img
                  src={image}
                  alt="Selected plant leaf"
                  className="
                    w-full
                    h-[280px]
                    md:h-[400px]
                    object-contain
                    bg-slate-50
                  "
                />

                <div className="absolute bottom-3 left-3 px-3 py-1.5 rounded-lg bg-black/50 backdrop-blur-sm text-white text-xs">
                  {t.readyAnalysis}
                </div>

              </div>


              <button
                onClick={handleDetectDisease}
                disabled={loading}

                className="
                  mt-5
                  w-full
                  py-4
                  rounded-2xl
                  bg-gradient-to-r from-emerald-600 to-green-600
                  hover:from-emerald-700 hover:to-green-700
                  disabled:opacity-70
                  disabled:cursor-not-allowed
                  text-white
                  font-bold
                  text-lg
                  shadow-xl
                  shadow-emerald-200
                  transition-all
                "
              >

                {loading ? (

                  <span className="flex items-center justify-center gap-3">

                    <span className="w-5 h-5 rounded-full border-2 border-white border-t-transparent animate-spin" />

                    {t.analyzing}

                  </span>

                ) : (

                  <span className="flex items-center justify-center gap-2">

                    <span>
                      🔍
                    </span>

                    {t.analyze}

                  </span>

                )}

              </button>

            </div>

          )}

        </div>


        {/* ================================================= */}
        {/* INVALID IMAGE */}
        {/* ================================================= */}

        {result &&
          result.status === "invalid_image" && (

          <div className="mt-8">

            <div className="bg-white rounded-3xl shadow-xl border border-amber-200 overflow-hidden">

              <div className="bg-gradient-to-r from-amber-50 to-yellow-50 p-6 md:p-8">

                <div className="flex items-start gap-4">

                  <div className="w-14 h-14 shrink-0 rounded-2xl bg-amber-100 flex items-center justify-center text-3xl">
                    📷
                  </div>

                  <div>

                    <p className="text-sm font-bold text-amber-600 uppercase tracking-wider">
                      {t.imageQuality}
                    </p>

                    <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900 mt-1">
                      {t.betterImage}
                    </h2>

                  </div>

                </div>


                <p className="mt-6 text-slate-600 leading-7">
                  {result.message}
                </p>


                <div className="mt-5 bg-white rounded-2xl p-5 border border-amber-100">

                  <p className="text-sm font-semibold text-slate-500">
                    💡 {t.recommendation}
                  </p>

                  <p className="mt-2 text-slate-700 leading-7">
                    {result.recommendation ||
                      t.clearLeaf}
                  </p>

                </div>

              </div>

            </div>

          </div>

        )}


        {/* ================================================= */}
        {/* UNCERTAIN RESULT */}
        {/* ================================================= */}

        {result &&
          result.status === "uncertain" && (

          <div className="mt-8">

            <div className="bg-white rounded-3xl shadow-xl border border-amber-200 overflow-hidden">

              <div className="bg-gradient-to-r from-amber-50 to-yellow-50 p-6 md:p-8">

                <div className="flex items-start gap-4">

                  <div className="w-14 h-14 shrink-0 rounded-2xl bg-amber-100 flex items-center justify-center text-3xl">
                    ⚠️
                  </div>

                  <div>

                    <p className="text-sm font-bold text-amber-600 uppercase tracking-wider">
                      {t.aiUncertain}
                    </p>

                    <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900 mt-1">
                      {t.unableIdentify}
                    </h2>

                  </div>

                </div>


                <p className="mt-6 text-slate-600 leading-7">
                  {result.message ||
                    t.clearLeaf}
                </p>


                <div className="mt-6 bg-white rounded-2xl p-5 border border-amber-100">

                  <div className="flex items-center justify-between">

                    <p className="text-sm font-semibold text-slate-500">
                      {t.modelConfidence}
                    </p>

                    <p className="text-2xl font-extrabold text-amber-600">
                      {result.confidence ||
                        "N/A"}
                    </p>

                  </div>


                  <div className="mt-3 h-2.5 bg-slate-100 rounded-full overflow-hidden">

                    <div
                      className="h-full bg-amber-400 rounded-full"
                      style={{
                        width:
                          typeof result.confidence ===
                          "number"
                            ? `${result.confidence}%`
                            : result.confidence ||
                              "0%",
                      }}
                    />

                  </div>

                </div>


                <div className="mt-5 bg-white rounded-2xl p-5 border border-amber-100">

                  <p className="text-sm font-semibold text-slate-500">
                    💡 {t.recommendation}
                  </p>

                  <p className="mt-2 text-slate-700 leading-7">
                    {result.recommendation ||
                      t.clearLeaf}
                  </p>

                </div>

              </div>


              {/* TOP PREDICTIONS */}

              {result.top_predictions &&
                result.top_predictions.length > 0 && (

                <div className="p-6 md:p-8">

                  <h3 className="text-lg font-bold text-slate-800">
                    {t.topPredictions}
                  </h3>

                  <p className="text-sm text-slate-400 mt-1">
                    {t.predictionDescription}
                  </p>


                  <div className="mt-5 space-y-3">

                    {result.top_predictions.map(
                      (prediction, index) => (

                      <div
                        key={`${prediction.class_name}-${index}`}
                        className="bg-slate-50 rounded-xl p-4"
                      >

                        <div className="flex items-center justify-between gap-4">

                          <p className="font-semibold text-slate-700 break-words">
                            {prediction.class_name}
                          </p>

                          <p className="font-bold text-slate-600 shrink-0">
                            {prediction.confidence}%
                          </p>

                        </div>

                      </div>

                    ))}

                  </div>

                </div>

              )}

            </div>

          </div>

        )}


        {/* ================================================= */}
        {/* REVIEW REQUIRED */}
        {/* ================================================= */}

        {result &&
          result.status === "review_required" && (

          <div className="mt-8">

            <div className="bg-white rounded-3xl shadow-xl border border-orange-200 overflow-hidden">

              <div className="bg-gradient-to-r from-orange-50 via-amber-50 to-yellow-50 p-6 md:p-8">

                <div className="flex items-start gap-4">

                  <div className="w-14 h-14 shrink-0 rounded-2xl bg-orange-100 flex items-center justify-center text-3xl">
                    ⚠️
                  </div>

                  <div>

                    <p className="text-sm font-bold text-orange-600 uppercase tracking-wider">
                      {t.reviewRequired}
                    </p>

                    <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900 mt-1">
                      {t.mismatchTitle}
                    </h2>

                  </div>

                </div>


                <p className="mt-6 text-slate-600 leading-7">
                  {result.message ||
                    t.mismatchMessage}
                </p>


                <div className="mt-5 bg-white rounded-2xl p-5 border border-orange-100">

                  <p className="text-sm font-bold text-orange-700">
                    🛡️ {t.safetyCheck}
                  </p>

                  <p className="mt-2 text-slate-600 leading-7">
                    {t.safetyMessage}
                  </p>

                </div>

              </div>


              <div className="p-6 md:p-8">

                <h3 className="text-lg font-bold text-slate-800">
                  {t.predictionComparison}
                </h3>


                <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">

                  {/* Crop Model */}

                  <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-5">

                    <p className="text-xs uppercase tracking-wider text-emerald-600 font-bold">
                      {t.cropModel}
                    </p>

                    <p className="mt-2 text-xl font-extrabold text-slate-800">

                      {result.predicted_crop ||
                        result.crop ||
                        t.unknown}

                    </p>


                    {result.crop_confidence !==
                      undefined && (

                      <p className="mt-2 text-sm text-slate-500">

                        {t.confidence}:{" "}

                        <span className="font-bold text-emerald-700">

                          {typeof result.crop_confidence ===
                          "number"
                            ? `${result.crop_confidence}%`
                            : result.crop_confidence}

                        </span>

                      </p>

                    )}

                  </div>


                  {/* Disease Model */}

                  <div className="bg-red-50 border border-red-100 rounded-2xl p-5">

                    <p className="text-xs uppercase tracking-wider text-red-600 font-bold">
                      {t.diseaseModel}
                    </p>

                    <p className="mt-2 text-xl font-extrabold text-slate-800 break-words">

                      {result.disease_name ||
                        result.disease ||
                        t.unknown}

                    </p>


                    {result.confidence !==
                      undefined && (

                      <p className="mt-2 text-sm text-slate-500">

                        {t.confidence}:{" "}

                        <span className="font-bold text-red-700">

                          {typeof result.confidence ===
                          "number"
                            ? `${result.confidence}%`
                            : result.confidence}

                        </span>

                      </p>

                    )}

                  </div>

                </div>


                {/* DISEASE CROP */}

                {result.disease_crop && (

                  <div className="mt-4 bg-slate-50 rounded-2xl p-5">

                    <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold">
                      {t.diseaseCrop}
                    </p>

                    <p className="mt-2 text-lg font-bold text-slate-800">
                      {result.disease_crop}
                    </p>

                  </div>

                )}


                {/* RECOMMENDATION */}

                <div className="mt-5 bg-amber-50 border border-amber-100 rounded-2xl p-5">

                  <p className="text-sm font-semibold text-amber-700">
                    💡 {t.recommendation}
                  </p>

                  <p className="mt-2 text-slate-700 leading-7">
                    {result.recommendation ||
                      t.mismatchRecommendation}
                  </p>

                </div>


                {/* TOP DISEASE PREDICTIONS */}

                {result.top_predictions &&
                  result.top_predictions.length > 0 && (

                  <div className="mt-6">

                    <h3 className="text-lg font-bold text-slate-800">
                      {t.topDiseasePredictions}
                    </h3>


                    <div className="mt-4 space-y-3">

                      {result.top_predictions.map(
                        (prediction, index) => (

                        <div
                          key={`${prediction.class_name}-${index}`}
                          className="bg-slate-50 rounded-xl p-4"
                        >

                          <div className="flex items-center justify-between gap-4">

                            <p className="font-semibold text-slate-700 break-words">
                              {prediction.class_name}
                            </p>

                            <p className="font-bold text-slate-600 shrink-0">
                              {prediction.confidence}%
                            </p>

                          </div>

                        </div>

                      ))}

                    </div>

                  </div>

                )}

              </div>

            </div>

          </div>

        )}


        {/* ================================================= */}
        {/* CONFIRMED RESULT */}
        {/* ================================================= */}

        {result &&
          result.status !== "uncertain" &&
          result.status !== "invalid_image" &&
          result.status !== "review_required" &&
          result.status !== "error" && (

          <div className="mt-8 space-y-5">

            {/* MAIN PREDICTION */}

            <div className="bg-white rounded-3xl shadow-xl border border-emerald-100 p-6 md:p-8">

              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">

                <div>

                  <div className="flex items-center gap-2">

                    <span className="w-2 h-2 rounded-full bg-emerald-500" />

                    <p className="text-sm font-bold text-emerald-600 uppercase tracking-wider">
                      {t.confirmedPrediction}
                    </p>

                  </div>


                  <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mt-2">
                    {result.disease_name ||
                      result.disease}
                  </h2>

                </div>


                <div className="min-w-[150px] bg-emerald-50 border border-emerald-100 rounded-2xl p-4">

                  <p className="text-sm text-slate-500">
                    {t.confidence}
                  </p>

                  <p className="text-3xl font-extrabold text-emerald-700 mt-1">
                    {result.confidence ||
                      "N/A"}
                  </p>

                </div>

              </div>


              {/* CONFIDENCE BAR */}

              <div className="mt-6">

                <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">

                  <div
                    className="h-full bg-gradient-to-r from-emerald-500 to-green-500 rounded-full transition-all duration-700"

                    style={{
                      width:
                        typeof result.confidence ===
                        "number"
                          ? `${result.confidence}%`
                          : result.confidence ||
                            "0%",
                    }}

                  />

                </div>

              </div>


              {/* CROP / CLASSIFICATION */}

              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">

                <div className="bg-slate-50 rounded-2xl p-5">

                  <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold">
                    {t.crop}
                  </p>

                  <p className="mt-2 text-lg font-bold text-slate-800">
                    {result.crop ||
                      result.predicted_crop ||
                      t.unknown}
                  </p>

                </div>


                <div className="bg-slate-50 rounded-2xl p-5">

                  <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold">
                    {t.classification}
                  </p>

                  <p className="mt-2 font-semibold text-slate-800 break-words">
                    {result.disease ||
                      result.class_name ||
                      t.unknown}
                  </p>

                </div>

              </div>

            </div>


            {/* SYMPTOMS */}

            <div className="bg-white rounded-2xl shadow-md border border-slate-100 p-6">

              <div className="flex items-center gap-3">

                <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
                  🩺
                </div>

                <h3 className="text-xl font-bold text-slate-800">
                  {t.symptoms}
                </h3>

              </div>

              <p className="mt-4 text-slate-600 leading-7">
                {result.symptoms ||
                  t.noSymptoms}
              </p>

            </div>


            {/* MANAGEMENT */}

            <div className="bg-white rounded-2xl shadow-md border border-slate-100 p-6">

              <div className="flex items-center gap-3">

                <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center">
                  🛠️
                </div>

                <h3 className="text-xl font-bold text-slate-800">
                  {t.management}
                </h3>

              </div>

              <p className="mt-4 text-slate-600 leading-7">
                {result.management ||
                  t.noManagement}
              </p>

            </div>


            {/* PREVENTION */}

            <div className="bg-white rounded-2xl shadow-md border border-slate-100 p-6">

              <div className="flex items-center gap-3">

                <div className="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center">
                  🛡️
                </div>

                <h3 className="text-xl font-bold text-slate-800">
                  {t.prevention}
                </h3>

              </div>

              <p className="mt-4 text-slate-600 leading-7">
                {result.prevention ||
                  t.noPrevention}
              </p>

            </div>


            {/* SOURCE */}

            {result.source && (

              <div className="bg-slate-50 rounded-2xl border border-slate-200 p-5">

                <p className="text-xs uppercase tracking-wider font-semibold text-slate-400">
                  {t.source}
                </p>

                <p className="mt-2 text-sm text-slate-600 break-words">
                  {result.source}
                </p>

              </div>

            )}

          </div>

        )}


        {/* ================================================= */}
        {/* ERROR */}
        {/* ================================================= */}

        {result &&
          result.status === "error" && (

          <div className="mt-8 bg-red-50 border border-red-200 rounded-2xl p-6">

            <div className="flex items-center gap-3">

              <div className="w-12 h-12 rounded-xl bg-red-100 flex items-center justify-center text-2xl">
                ❌
              </div>

              <div>

                <p className="text-sm font-bold text-red-600 uppercase tracking-wider">
                  {t.error}
                </p>

                <h2 className="text-xl font-bold text-slate-800">
                  {t.detectionFailed}
                </h2>

              </div>

            </div>


            <p className="mt-4 text-slate-600">
              {result.error ||
                t.errorMessage}
            </p>

          </div>

        )}

      </div>
    </div>
  );
}

export default DiseaseDetection;