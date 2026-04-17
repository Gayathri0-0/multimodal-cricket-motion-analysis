import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# =========================
# 🔹 DUMMY DATASET
# =========================
data = {
    "momentum": [
        # GOOD (high momentum)
        0.055, 0.052, 0.058,

        # POOR (low momentum)
        0.005, 0.008, 0.01,

        # AVERAGE
        0.03, 0.028, 0.032,

        # MIXED
        0.05, 0.027, 0.009
    ],

    "head_stability": [
        # GOOD (low movement)
        0.015, 0.02, 0.018,

        # POOR (high movement)
        0.06, 0.055, 0.05,

        # AVERAGE
        0.035, 0.04, 0.03,

        # MIXED
        0.02, 0.038, 0.052
    ],

    "leg_bracing": [
        # GOOD (LOW angle change → strong bracing)
        3, 4, 5,

        # POOR (HIGH angle change → collapse)
        15, 18, 17,

        # AVERAGE
        8, 10, 9,

        # MIXED
        6, 11, 16
    ],

    "alignment": [
        # GOOD (low misalignment)
        0.015, 0.02, 0.018,

        # POOR (high misalignment)
        0.06, 0.055, 0.05,

        # AVERAGE
        0.035, 0.04, 0.03,

        # MIXED
        0.02, 0.038, 0.052
    ],

    "performance": [
        2, 2, 2,   # GOOD
        0, 0, 0,   # POOR
        1, 1, 1,   # AVERAGE
        2, 1, 0    # MIXED
    ]
}


df = pd.DataFrame(data)

print("=== DATASET ===")
print(df)

# =========================
# 🔹 FEATURES & LABEL
# =========================

X = df[["momentum", "head_stability", "leg_bracing", "alignment"]]
y = df["performance"]

# =========================
# 🔹 SCALING
# =========================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# 🔹 MODEL TRAINING
# =========================

model = LogisticRegression()
model.fit(X_scaled, y)

print("\nModel trained successfully!")

# =========================
# 🔹 SAVE MODEL (optional)
# =========================

joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

# =========================
# 🔹 SHOW MODEL WEIGHTS
# =========================

print("\n=== MODEL WEIGHTS ===")
for feature, coef in zip(X.columns, model.coef_[0]):
    print(f"{feature}: {coef:.3f}")



# =========================
# 🔹 MULTIPLE TEST PREDICTIONS
# =========================

labels = ["Poor", "Average", "Good"]


test_cases = [
    {
        "name": "Good Delivery",
        "data": {
            "momentum": 0.05,          # high ✅
            "head_stability": 0.02,    # low movement ✅
            "leg_bracing": 4,          # LOW angle change ✅
            "alignment": 0.02          # low misalignment ✅
        }
    },
    {
        "name": "Average Delivery",
        "data": {
            "momentum": 0.028,         # medium
            "head_stability": 0.035,   # medium
            "leg_bracing": 10,         # medium
            "alignment": 0.035         # medium
        }
    },
    {
        "name": "Poor Delivery",
        "data": {
            "momentum": 0.008,         # low ❌
            "head_stability": 0.055,   # high movement ❌
            "leg_bracing": 16,         # HIGH collapse ❌
            "alignment": 0.05          # high misalignment ❌
        }
    }
]


print("\n=== TEST PREDICTIONS ===")

for case in test_cases:
    sample_df = pd.DataFrame([case["data"]])
    sample_scaled = scaler.transform(sample_df)
    pred = model.predict(sample_scaled)[0]

    print(f"\n{case['name']}:")
    print(sample_df)
    print("Predicted:", labels[pred])


