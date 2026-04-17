import pandas as pd
import joblib

# =========================
# 🔹 LOAD MODEL
# =========================

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

print("Model loaded successfully!")

# =========================
# 🔹 LOAD CSV DATA
# =========================

df = pd.read_csv("bowling_data.csv")

# =========================
# 🔹 TRANSFORM FEATURES (IMPORTANT)
# =========================

df["head_stability"] = 1 - df["head_stability"]
df["alignment"] = 1 - df["alignment"]
df["leg_bracing"] = 1 - (df["leg_bracing"] / 20)

# Make sure columns match
X = df[["momentum", "head_stability", "leg_bracing", "alignment"]]

# =========================
# 🔹 SCALE DATA
# =========================

X_scaled = scaler.transform(X)

# =========================
# 🔹 PREDICTION
# =========================

predictions = model.predict(X_scaled)

# =========================
# 🔹 MAP OUTPUT LABELS
# =========================

def label_map(x):
    if x == 0:
        return "Poor"
    elif x == 1:
        return "Average"
    else:
        return "Good"

df["Predicted_Performance"] = [label_map(p) for p in predictions]

# =========================
# 🔹 WEIGHTED SCORE (OPTIONAL)
# =========================

df["Weighted_Score"] = (
    0.4 * df["momentum"] +
    0.3 * (1 - df["head_stability"]) +  
    0.2 * (df["leg_bracing"] / 20) +
    0.1 * (1 - df["alignment"])
)

# =========================
# 🔹 OUTPUT
# =========================

print("\nPredictions:\n")
print(df[["momentum", "head_stability", "leg_bracing", "alignment",
          "Weighted_Score", "Predicted_Performance"]])
