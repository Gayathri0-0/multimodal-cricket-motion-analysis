import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bowling_data.csv")

momentum = df["momentum"]

# 🔥 Moving average (smoothing)
window_size = 20
smooth_momentum = momentum.rolling(window=window_size).mean()

plt.plot(smooth_momentum)
plt.title("Smoothed Momentum Over Time")
plt.xlabel("Frame")
plt.ylabel("Momentum")
plt.grid()

plt.show()
