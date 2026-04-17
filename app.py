import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 🔹 LOAD MODEL
# =========================

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

labels = ["Poor", "Average", "Good"]

# =========================
# 🔹 PAGE CONFIG
# =========================

st.set_page_config(page_title="Bowling Analyzer", layout="wide")

st.title("🏏 Bowling Performance Analyzer")
st.markdown("### AI-powered Biomechanics Evaluation")

# =========================
# 🔹 LAYOUT
# =========================

col1, col2 = st.columns(2)

# =========================
# 🔹 INPUT SECTION
# =========================

with col1:
    st.subheader("🎛 Input Parameters")

    momentum = st.slider("Momentum", 0.0, 0.06, 0.03)
    head = st.slider("Head Stability", 0.0, 0.07, 0.03)
    leg = st.slider("Leg Bracing", 0, 20, 10)
    alignment = st.slider("Alignment", 0.0, 0.07, 0.03)

# =========================
# 🔹 OUTPUT SECTION
# =========================

with col2:
    st.subheader("📊 Results")

    if st.button("Analyze Delivery"):

        # Create input dataframe
        df = pd.DataFrame([{
            "momentum": momentum,
            "head_stability": head,
            "leg_bracing": leg,
            "alignment": alignment
        }])

        # =========================
        # 🔹 APPLY SAME TRANSFORMATION
        # =========================

        df["head_stability"] = 1 - df["head_stability"]
        df["alignment"] = 1 - df["alignment"]
        df["leg_bracing"] = 1 - (df["leg_bracing"] / 20)

        # Scale + Predict
        scaled = scaler.transform(df)
        pred = model.predict(scaled)[0]


       
        # =========================
        # 🔹 SCORE (OUT OF 100)
        # =========================

        score = (
            0.4 * momentum +
            0.3 * (1 - head) +
            0.2 * (1 - leg / 20) +
            0.1 * (1 - alignment)
        )

        score_percent = int(score * 100)

        st.metric("Performance Score", f"{score_percent}/100")
        st.progress(score_percent / 100)

        st.success(f"Prediction: {labels[pred]}")

        # =========================
        # 🔹 FEATURE CONTRIBUTION
        # =========================

        st.subheader("🔍 Feature Contribution")

        coeffs = model.coef_[0]
        feature_names = ["Momentum", "Head Stability", "Leg Bracing", "Alignment"]

        input_values = scaled[0]

        for i, name in enumerate(feature_names):
            contribution = coeffs[i] * input_values[i]

            if contribution > 0:
                st.markdown(f"🟢 **{name}**: {contribution:.3f}")
            else:
                st.markdown(f"🔴 **{name}**: {contribution:.3f}")

            st.progress(min(abs(contribution), 1.0))

        # =========================
        # 🔹 TOP FACTOR INSIGHT
        # =========================

        contributions = [
            coeffs[i] * input_values[i] for i in range(len(feature_names))
        ]

        max_impact_index = contributions.index(max(contributions, key=abs))
        st.info(f"🔎 Most influential factor: {feature_names[max_impact_index]}")

        # =========================
        # 🔹 EXPLANATION
        # =========================

        st.subheader("🧠 Explanation")

        if momentum < 0.02:
            st.write("• Low momentum reduces performance")

        if head > 0.04:
            st.write("• Head instability affects control")

        if leg < 8:
            st.write("• Poor leg bracing (knee collapse) reduces power")

        if alignment > 0.04:
            st.write("• Poor alignment affects efficiency")

        if (momentum >= 0.02 and head <= 0.04 and leg >= 8 and alignment <= 0.04):
            st.write("• All metrics are in optimal range")

        # =========================
        # 🔹 FEEDBACK
        # =========================

        st.subheader("🏏 Coaching Feedback")

        if pred == 2:
            st.success("Excellent delivery. Maintain consistency.")
        elif pred == 1:
            st.warning("Decent delivery. Improve key areas.")
        else:
            st.error("Poor delivery. Focus on fundamentals.")

# =========================
# 🔹 MOMENTUM GRAPH
# =========================

st.subheader("📈 Momentum Analysis")

graph_type = st.radio("Select Type", ["Good Delivery", "Poor Delivery"])

if graph_type == "Good Delivery":
    speeds = [0.01, 0.014, 0.018, 0.023, 0.021, 0.027, 0.032, 0.038, 0.042, 0.047, 0.05]
else:
    speeds = [0.02, 0.018, 0.022, 0.019, 0.021, 0.02, 0.023, 0.021, 0.022, 0.02]

fig, ax = plt.subplots()
ax.plot(speeds, marker='o')

peak_value = max(speeds)
peak_index = speeds.index(peak_value)

ax.scatter(peak_index, peak_value)
ax.text(peak_index, peak_value, " Peak", fontsize=10)

ax.set_title("Momentum (Speed over Time)")
ax.set_xlabel("Frame")
ax.set_ylabel("Speed")

st.pyplot(fig)

# =========================
# 🔹 FOOTER
# =========================

st.write("---")
st.markdown("Built using AI + Biomechanics + Machine Learning")
