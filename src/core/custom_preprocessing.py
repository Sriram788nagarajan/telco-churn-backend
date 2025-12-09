import pandas as pd

def missing_handle(df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.copy()
    # Convert TotalCharges to numeric and fill missing with 0
    df1["TotalCharges"] = pd.to_numeric(df1["TotalCharges"], errors="coerce")
    df1["TotalCharges"] = df1["TotalCharges"].fillna(0)
    return df1

def drop_useless_cols(df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.copy()
    df1.drop(columns=["customerID"], errors="ignore", inplace=True)
    return df1

def internet_features(df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.copy()

    df1["HasInternet"] = (df1["InternetService"] == "No").astype(int)

    internet_service_cols = [
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]

    for col in internet_service_cols:
        df1[col + "_Active"] = (
            (df1[col] == "Yes") & (df1["HasInternet"] == 0)
        ).astype(int)

    df1.drop(internet_service_cols, axis=1, inplace=True)
    return df1

def phone_features(df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.copy()

    df1["HasPhone"] = (df1["PhoneService"] == "No").astype(int)
    df1["MultipleLinesActive"] = (
        (df1["MultipleLines"] == "Yes") & (df1["HasPhone"] == 0)
    ).astype(int)

    df1.drop("MultipleLines", axis=1, inplace=True)
    df1["PhoneService"] = (df1["PhoneService"] == "Yes").astype(int)

    return df1

def binary_features(df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.copy()

    df1["gender"] = (df1["gender"] == "Male").astype(int)
    df1["Partner"] = (df1["Partner"] == "Yes").astype(int)
    df1["Dependents"] = (df1["Dependents"] == "Yes").astype(int)
    df1["PaperlessBilling"] = (df1["PaperlessBilling"] == "Yes").astype(int)

    return df1

def ordinal_features(df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.copy()

    df1["Contract"] = df1["Contract"].map(
        {
            "Month-to-month": 0,
            "One year": 1,
            "Two year": 2,
        }
    )

    return df1
