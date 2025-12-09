import React, { useState } from "react";
import axios from "axios";

const categoricalOptions = {
  gender: ["Female", "Male"],
  Partner: ["Yes", "No"],
  Dependents: ["No", "Yes"],
  PhoneService: ["No", "Yes"],
  MultipleLines: ["No phone service", "No", "Yes"],
  InternetService: ["DSL", "Fiber optic", "No"],
  OnlineSecurity: ["No", "Yes", "No internet service"],
  OnlineBackup: ["Yes", "No", "No internet service"],
  DeviceProtection: ["No", "Yes", "No internet service"],
  TechSupport: ["No", "Yes", "No internet service"],
  StreamingTV: ["No", "Yes", "No internet service"],
  StreamingMovies: ["No", "Yes", "No internet service"],
  Contract: ["Month-to-month", "One year", "Two year"],
  PaperlessBilling: ["Yes", "No"],
  PaymentMethod: [
    "Electronic check",
    "Mailed check",
    "Bank transfer (automatic)",
    "Credit card (automatic)"
  ],
};

const PredictForm = () => {
  const [formData, setFormData] = useState({
    gender: "",
    SeniorCitizen: "",
    Partner: "",
    Dependents: "",
    tenure: "",
    PhoneService: "",
    MultipleLines: "",
    InternetService: "",
    OnlineSecurity: "",
    OnlineBackup: "",
    DeviceProtection: "",
    TechSupport: "",
    StreamingTV: "",
    StreamingMovies: "",
    Contract: "",
    PaperlessBilling: "",
    PaymentMethod: "",
    MonthlyCharges: "",
    TotalCharges: ""
  });

  const [errors, setErrors] = useState({});
  const [result, setResult] = useState(null);

  const validateForm = () => {
    let newErrors = {};

    // Required categorical validations
    Object.keys(categoricalOptions).forEach((key) => {
      if (!formData[key]) newErrors[key] = "This field is required.";
    });

    // SeniorCitizen must be 0 or 1
    if (formData.SeniorCitizen !== "0" && formData.SeniorCitizen !== "1") {
      newErrors.SeniorCitizen = "Enter 0 (Not a senior) or 1 (Senior citizen).";
    }

    // Numeric validations
    ["tenure", "MonthlyCharges", "TotalCharges"].forEach((field) => {
      if (!formData[field]) {
        newErrors[field] = "This value is required.";
      } else if (isNaN(formData[field])) {
        newErrors[field] = "Must be a valid number.";
      }
    });

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) {
      alert("Please correct the highlighted errors.");
      return;
    }

    try {
      const payload = {
        ...formData,
        SeniorCitizen: Number(formData.SeniorCitizen),
        tenure: Number(formData.tenure),
        MonthlyCharges: Number(formData.MonthlyCharges),
        TotalCharges: Number(formData.TotalCharges),
      };

      const res = await axios.post("http://127.0.0.1:8000/predict/", payload);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Prediction failed.");
    }
  };

  const updateField = (field, value) => {
    setFormData({
      ...formData,
      [field]: value
    });
  };

  return (
    <div style={{ width: "500px", margin: "30px auto", padding: "20px" }}>
      <h2>Telco Churn Prediction</h2>

      {/* Render categorical dropdowns */}
      {Object.keys(categoricalOptions).map((field) => (
        <div key={field} style={{ marginBottom: "12px" }}>
          <label>{field}</label>
          <select
            value={formData[field]}
            onChange={(e) => updateField(field, e.target.value)}
            style={{ width: "100%", padding: "6px" }}
          >
            <option value="">Select {field}</option>
            {categoricalOptions[field].map((val) => (
              <option key={val} value={val}>
                {val}
              </option>
            ))}
          </select>
          {errors[field] && (
            <div style={{ color: "red", fontSize: "13px" }}>
              {errors[field]}
            </div>
          )}
        </div>
      ))}

      {/* SeniorCitizen */}
      <div style={{ marginBottom: "12px" }}>
        <label>SeniorCitizen (0 = Not senior, 1 = Senior citizen)</label>
        <input
          type="number"
          value={formData.SeniorCitizen}
          onChange={(e) => updateField("SeniorCitizen", e.target.value)}
          style={{ width: "100%", padding: "6px" }}
        />
        {errors.SeniorCitizen && (
          <div style={{ color: "red", fontSize: "13px" }}>
            {errors.SeniorCitizen}
          </div>
        )}
      </div>

      {/* Numeric fields */}
      {["tenure", "MonthlyCharges", "TotalCharges"].map((field) => (
        <div key={field} style={{ marginBottom: "12px" }}>
          <label>{field}</label>
          <input
            type="number"
            value={formData[field]}
            onChange={(e) => updateField(field, e.target.value)}
            style={{ width: "100%", padding: "6px" }}
          />
          {errors[field] && (
            <div style={{ color: "red", fontSize: "13px" }}>
              {errors[field]}
            </div>
          )}
        </div>
      ))}

      <button
        onClick={handleSubmit}
        style={{ width: "100%", padding: "10px", marginTop: "15px" }}
      >
        Predict
      </button>

      {result && (
        <div style={{ marginTop: "20px", padding: "15px", border: "1px solid black" }}>
          <h3>Prediction Result</h3>
          <p>Churn Probability: {result.churn_probability.toFixed(4)}</p>
          <p>Churn Label: {result.churn_label}</p>
        </div>
      )}
    </div>
  );
};

export default PredictForm;
