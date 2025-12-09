import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from src.core.custom_preprocessing import (
    missing_handle,
    drop_useless_cols,
    internet_features,
    phone_features,
    binary_features,
    ordinal_features,
)

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # points to src/
DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "model.pkl"
THRESHOLD_PATH = MODEL_DIR / "threshold.json"

# ----------------------------
# Load data
# ----------------------------
print(f"Loading data from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

# ----------------------------
# Target encoding
# ----------------------------
y = (df["Churn"] == "Yes").astype(int)
X = df.drop(columns=["Churn"])

# ----------------------------
# Column groups AFTER preprocessing
# ----------------------------
# After applying our feature functions, we know what columns will exist.
# Numeric / ordinal columns (to be scaled)
numeric_cols = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "Contract",
]

# Categorical (nominal) columns to OneHotEncode
categorical_onehot_cols = ["InternetService", "PaymentMethod"]

# ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ("onehot", OneHotEncoder(handle_unknown="ignore"), categorical_onehot_cols),
        ("scale", StandardScaler(), numeric_cols),
    ],
    remainder="passthrough",
)

# ----------------------------
# Full Pipeline
# ----------------------------
clf = Pipeline(
    steps=[
        ("missing", FunctionTransformer(missing_handle, validate=False)),
        ("drop", FunctionTransformer(drop_useless_cols, validate=False)),
        ("internet", FunctionTransformer(internet_features, validate=False)),
        ("phone", FunctionTransformer(phone_features, validate=False)),
        ("binary", FunctionTransformer(binary_features, validate=False)),
        ("ordinal", FunctionTransformer(ordinal_features, validate=False)),
        ("preprocessor", preprocessor),
        (
            "model",
            XGBClassifier(
                n_estimators=300,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                eval_metric="logloss",
                random_state=42,
            ),
        ),
    ]
)

# ----------------------------
# Train / Test split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Fitting pipeline...")
clf.fit(X_train, y_train)
print("Training complete.")

# ----------------------------
# Basic evaluation (just to sanity check)
# ----------------------------
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]

print("\nClassification report:\n")
print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# ----------------------------
# Save model
# ----------------------------
print(f"\nSaving model to: {MODEL_PATH}")
joblib.dump(clf, MODEL_PATH)
print("Model saved.")

# ----------------------------
# Save threshold
# ----------------------------
# TODO: replace this with YOUR chosen threshold from earlier experiments
BEST_THRESHOLD = 0.25  # <<< PUT YOUR REAL VALUE HERE

print(f"Saving threshold ({BEST_THRESHOLD}) to: {THRESHOLD_PATH}")
with open(THRESHOLD_PATH, "w") as f:
    json.dump({"threshold": BEST_THRESHOLD}, f)

print("Threshold saved.")
print("\nALL DONE.")
