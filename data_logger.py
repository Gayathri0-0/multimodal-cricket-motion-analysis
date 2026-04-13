import pandas as pd

data = []

def clear_data():
    global data
    data = []

def log_data(head, align, momentum, leg):
    data.append([head, align, momentum, leg])

def save_data():
    df = pd.DataFrame(data, columns=[
        "head_stability",
        "alignment",
        "momentum",
        "leg_bracing"
    ])
    df.to_csv("bowling_data.csv", index=False)
    print("Data saved!")

