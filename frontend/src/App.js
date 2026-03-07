import React, { useState } from "react";
import axios from "axios";

const InputField = ({ label, name, placeholder, type = "text", onChange }) => (
  <div className="flex flex-col gap-1">
    <label className="text-sm font-medium text-gray-600">{label}</label>
    <input
      name={name}
      type={type}
      placeholder={placeholder}
      onChange={onChange}
      className="border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
    />
  </div>
);

function App() {
  const [formData, setFormData] = useState({
    AIRLINE: "",
    ORIGIN_AIRPORT: "",
    DESTINATION_AIRPORT: "",
    DEPARTURE_TIME: "",
    DISTANCE: "",
    DAY_OF_WEEK: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      ...formData,
      DEPARTURE_TIME: Number(formData.DEPARTURE_TIME),
      DISTANCE: Number(formData.DISTANCE),
      DAY_OF_WEEK: Number(formData.DAY_OF_WEEK),
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        payload,
      );
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Prediction failed. Please check your inputs and try again.");
    } finally {
      setLoading(false);
    }
  };

  const delayed = result?.data?.prediction === 1;
  const probability = result
    ? (result.data.delay_probability * 100).toFixed(1)
    : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
      <div className="w-full max-w-lg">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="text-5xl mb-3">✈️</div>
          <h1 className="text-3xl font-bold text-gray-800">
            Flight Delay Predictor
          </h1>
          <p className="text-gray-500 mt-1 text-sm">
            Enter flight details to predict delay probability
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div className="grid grid-cols-2 gap-4">
              <InputField
                label="Airline Code"
                name="AIRLINE"
                placeholder="e.g. AA"
                onChange={handleChange}
              />
              <InputField
                label="Day of Week"
                name="DAY_OF_WEEK"
                placeholder="1 = Mon, 7 = Sun"
                type="number"
                onChange={handleChange}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <InputField
                label="Origin Airport"
                name="ORIGIN_AIRPORT"
                placeholder="e.g. JFK"
                onChange={handleChange}
              />
              <InputField
                label="Destination Airport"
                name="DESTINATION_AIRPORT"
                placeholder="e.g. LAX"
                onChange={handleChange}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <InputField
                label="Departure Time"
                name="DEPARTURE_TIME"
                placeholder="e.g. 900"
                type="number"
                onChange={handleChange}
              />
              <InputField
                label="Distance (miles)"
                name="DISTANCE"
                placeholder="e.g. 2475"
                type="number"
                onChange={handleChange}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold py-2.5 rounded-lg transition text-sm"
            >
              {loading ? "Predicting..." : "Predict Delay"}
            </button>
          </form>
        </div>

        {/* Error */}
        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-700 rounded-xl px-5 py-4 text-sm">
            {error}
          </div>
        )}

        {/* Result Card */}
        {result && (
          <div className="mt-4 bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">
              Prediction Result
            </h2>

            <div
              className={`inline-block px-4 py-1.5 rounded-full text-sm font-semibold mb-4 ${
                delayed
                  ? "bg-red-100 text-red-700"
                  : "bg-green-100 text-green-700"
              }`}
            >
              {delayed ? "⚠️ Likely Delayed" : "✅ On Time"}
            </div>

            <p className="text-sm text-gray-500 mb-2">Delay Probability</p>
            <div className="w-full bg-gray-100 rounded-full h-3 mb-1">
              <div
                className={`h-3 rounded-full transition-all ${
                  delayed ? "bg-red-500" : "bg-green-500"
                }`}
                style={{ width: `${probability}%` }}
              />
            </div>
            <p className="text-right text-sm font-medium text-gray-700">
              {probability}%
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
