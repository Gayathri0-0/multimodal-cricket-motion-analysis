import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# ==============================
# 🔥 STEP 1: TRAIN MODEL (same dummy data)
# ==============================

data = {
    "head_stability": [0.01, 0.02, 0.015, 0.05, 0.06, 0.04, 0.03, 0.07, 0.025, 0.035],
    "alignment":      [0.01, 0.015, 0.02, 0.05, 0.045, 0.04, 0.03, 0.06, 0.02, 0.035],
    "momentum":       [0.035, 0.03, 0.04, 0.015, 0.01, 0.02, 0.025, 0.012, 0.03, 0.02],
    "leg_bracing":    [15, 12, 18, 5, 3, 8, 10, 4, 14, 9],
    "performance":    [2, 2, 2, 0, 0, 1, 1, 0, 2, 1]
}

df = pd.DataFrame(data)

X = df[["head_stability", "alignment", "momentum", "leg_bracing"]]
y = df["performance"]

model = DecisionTreeClassifier()
model.fit(X, y)

print("Model trained.")

# ==============================
# 🔥 STEP 2: LOAD REAL CSV
# ==============================

real_data = pd.read_csv("bowling_data.csv")

print("\n=== REAL DATA ===")
print(real_data)

# ==============================
# 🔥 STEP 3: PREDICT
# ==============================

prediction = model.predict(real_data)

labels = ["Poor", "Average", "Good"]

print("\n=== FINAL RESULT ===")
for i, pred in enumerate(prediction):
    print(f"Delivery {i+1}: {labels[pred]}")
