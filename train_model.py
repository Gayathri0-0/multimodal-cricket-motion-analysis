import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt

# ==============================
# 🔥 STEP 1: CREATE DUMMY DATASET
# ==============================

data = {
    "head_stability": [0.01, 0.02, 0.015, 0.05, 0.06, 0.04, 0.03, 0.07, 0.025, 0.035],
    "alignment":      [0.01, 0.015, 0.02, 0.05, 0.045, 0.04, 0.03, 0.06, 0.02, 0.035],
    "momentum":       [0.035, 0.03, 0.04, 0.015, 0.01, 0.02, 0.025, 0.012, 0.03, 0.02],
    "leg_bracing":    [15, 12, 18, 5, 3, 8, 10, 4, 14, 9],
    "performance":    [2, 2, 2, 0, 0, 1, 1, 0, 2, 1]
}

df = pd.DataFrame(data)

print("=== DATASET ===")
print(df)

# ==============================
# 🔥 STEP 2: TRAIN MODEL
# ==============================

X = df[["head_stability", "alignment", "momentum", "leg_bracing"]]
y = df["performance"]

model = DecisionTreeClassifier()
model.fit(X, y)

print("\nModel trained successfully!")

# ==============================
# 🔥 STEP 3: TEST PREDICTION
# ==============================

# Example test case
test_data = pd.DataFrame([{
    "head_stability": 0.02,
    "alignment": 0.02,
    "momentum": 0.03,
    "leg_bracing": 14
}])

prediction = model.predict(test_data)

# Convert to readable output
labels = ["Poor", "Average", "Good"]

print("\n=== PREDICTION ===")
print("Predicted Class:", labels[prediction[0]])

# ==============================
# 🔥 STEP 4: VISUALIZE MODEL (OPTIONAL BUT POWERFUL)
# ==============================

plt.figure(figsize=(12, 6))
tree.plot_tree(
    model,
    feature_names=X.columns,
    class_names=["Poor", "Average", "Good"],
    filled=True
)
plt.title("Decision Tree Visualization")
plt.show()
