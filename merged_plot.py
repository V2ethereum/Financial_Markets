import pandas as pd
import matplotlib.pyplot as plt


'''
# Plot the closing prices over time
plt.figure(figsize=(10, 6))
plt.plot(brazil["Date"], brazil["Close"], color="blue", label="JSE All Share Index (Close Price)")

plt.title("South Africa JSE All Share Index Over Time")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.tight_layout()
plt.show()
'''



'''
# Yearwise HURST exponent plots
h_1 = pd.read_csv("/home/student/Coding/Database/China.csv")
h_1.set_index('Year', inplace=True)
h_2 = pd.read_csv("/home/student/Coding/Database/China_2.csv")
h_2.set_index('Year', inplace = True)

h_merged = pd.merge(h_1, h_2, left_index=True, right_index=True, how="inner")

plt.plot(h_merged.index, h_merged["h(1)_x"], marker="o", linestyle="-", color="blue", label="h(1)")
plt.plot(h_merged.index, h_merged["h(1)_y"], marker="o", linestyle="-", color="red", label="h(2)")

# Labels and Title
plt.xlabel("Year")
plt.ylabel("h(q)")
plt.title("China - Hurst Exponent (h) for different values of q")
plt.legend()
plt.grid(True)
plt.show()
'''





'''
hurst = pd.read_csv("/home/student/Coding/Database/SA_f(α).csv")
hurst.set_index('q', inplace=True)

plt.plot(hurst.index, hurst["h(q)"], marker="o", linestyle="-", color="black", label="τ(q)")
plt.xlabel("q")
plt.ylabel("h(q)")
plt.title("South Africa - Hurst Exponent(h(q)) for different values of q")
plt.legend()
plt.grid(True)
plt.show()
'''


'''
multi = pd.read_csv("/home/student/Coding/Database/SA_f(α).csv")
multi.set_index('q', inplace=True)

plt.plot(multi["α(q)"], multi["f(α)"], marker="o", linestyle="-", color="black")
plt.xlabel("α(q)")
plt.ylabel("f(α)")
plt.title("South Africa - Multifractal spectrum")
plt.legend()
plt.grid(True)
plt.show()
'''

'''
datasets = {
    "Brazil": pd.read_csv("/home/student/Coding/Database/Brazil_f(α).csv"),
    "Russia": pd.read_csv("/home/student/Coding/Database/Russia_f(α).csv"),
    "India": pd.read_csv("/home/student/Coding/Database/India_f(α).csv"),
    "China": pd.read_csv("/home/student/Coding/Database/China_f(α).csv"),
    "SA": pd.read_csv("/home/student/Coding/Database/SA_f(α).csv"),
    "USA": pd.read_csv("/home/student/Coding/Database/USA_f(α).csv")
}

# Set up plot
plt.figure(figsize=(10, 6))
colors = ["red", "blue", "green", "orange", "purple", "Black"]

# Loop through each dataset and plot
for (country, df), color in zip(datasets.items(), colors):
    alpha = df["α(q)"]  # or df["alpha(q)"] if column uses that
    f_alpha = df["f(α)"]
    plt.plot(alpha, f_alpha, label=country, color=color)

# Customize plot
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$f(\alpha)$")
plt.title("Multifractal Spectrum Comparison Across Countries")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
'''

import pandas as pd

# Step 1: Load original file
df = pd.read_csv("/home/student/Coding/Database/USA_data.csv")

# Step 2: Convert 'Date' to datetime and reformat to 'YYYY-MM-DD'
df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="coerce")
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

# Step 3: Save the cleaned CSV
df.to_csv("/home/student/Coding/Database/USA_data_cleaned.csv", index=False)

print("Saved cleaned USA dataset with formatted dates.")
