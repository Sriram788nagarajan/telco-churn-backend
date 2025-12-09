import json
import os
from pathlib import Path

import joblib
import pandas as pd

# Important: import this so that custom_preprocessing functions are registered
import core.custom_preprocessing  # noqa: F401

BASE_DIR = Path(__file__).resolve().parent.parent  # src/
MODEL_PATH = BASE_DIR / "model" / "model.pkl"
THRESHOLD_PATH = BASE_DIR / "model" / "threshold.json"

print(f"Loading model from: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

print(f"Loading threshold from: {THRESHOLD_PATH}")
with open(THRESHOLD_PATH, "r") as f:
    threshold = json.load(f)["threshold"]


def predict_single(input_dict: dict):
    """
    Takes raw customer input (dict), returns (label, probability)
    """
    df = pd.DataFrame([input_dict])
    prob = float(model.predict_proba(df)[0, 1])
    label = 1 if prob >= threshold else 0
    return label, prob
