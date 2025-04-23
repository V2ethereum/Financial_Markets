import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

datasets = {
    "Brazil": pd.read_csv("/home/student/Coding/Database/Brazil_data.csv", parse_dates=["Date"]),
    "Russia": pd.read_csv("/home/student/Coding/Database/Russia_data.csv", parse_dates=["Date"]),
    "India": pd.read_csv("/home/student/Coding/Database/India_data.csv", parse_dates=["Date"]),
    "China": pd.read_csv("/home/student/Coding/Database/China_data.csv", parse_dates=["Date"]),
    "SA": pd.read_csv("/home/student/Coding/Database/SA_data.csv", parse_dates=["Date"]),
    "USA": pd.read_csv("/home/student/Coding/Database/USA_data.csv", parse_dates=["Date"]),
}

#print(datasets["SA"].head())

#Log-Retruns
for contry, df in datasets.items():
    df["Log_rt"] = np.log(df["Close"]/df["Close"].shift(1)) #Column named Log_rt is added in dataset



'''
#Calculating Statistics
stats = {}

def compute_stats(df):
    return { 
        "Mean" : df["Log_rt"].mean(),
        "STD": df["Log_rt"].std(),
        "Skewness": df["Log_rt"].skew(),
        "Kurtosis": df["Log_rt"].kurt(),
    }

for country, df in datasets.items():
    stats[country] = compute_stats(df)

stats_df = pd.DataFrame(stats) # Convert to DataFrame for better visualization

#print(stats_df)
#stats_df.to_csv("log_return_statistics.csv", index=True)
'''


#First step of MFDFA

def compute_profile(df):
    df["profile"] = (df["Log_rt"] - df["Log_rt"].mean()).cumsum()
    return df

for country, df in datasets.items():
    datasets[country] = compute_profile(df) #Add profile column 

'''
for country, df in datasets.items():
    plt.figure(figsize=(12, 6))
    
    # Plot Log Returns and Profile on the same chart
    plt.plot(df.index, df["Log_rt"], label="Log Returns", color='black')
    plt.plot(df.index, df["profile"], label="Profile", color='gray', linestyle='dashed')
    
    # Add title, labels, and legend
    plt.title(f"{country} - Log Returns & Profile", fontsize=14, pad=10)
    plt.xlabel("Sample Number (Index)", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

'''


for country, df in datasets.items():
    df["profile"] = df["profile"].fillna(0)  # Replace NaN with 0 (or use interpolation)



'''
# Detrending + polyfit for each country

from numpy.polynomial.polynomial import Polynomial

df = datasets["USA"]
profile = df["profile"].values
scales = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
#scales = np.arange(2, 2050, 2)  

q_values = np.arange(-5, 5, 0.2)
#q_values = [-2, -1, 0, 1, 2]  
F_q = {q: [] for q in q_values}

for s in scales:
    num_segments = len(profile) // s
    F_s_scale = []
    
    for v in range(num_segments):
        segment = profile[v * s : (v + 1) * s]  
        x = np.arange(s)  #Numbering each element in segment
        
        poly_coeffs = np.polyfit(x, segment, deg=2) 
        poly_trend = np.polyval(poly_coeffs, x) 
        
        fluctuation = (segment - poly_trend) ** 2  
        F_s_scale.append(np.mean(fluctuation))  # Mean squared fluctuation
    
    # Compute F_q(s)
    for q in q_values:
        if q == 0:
            F_q[q].append(np.exp(0.5 * np.mean(np.log(F_s_scale))))  # Log-averaging for q=0
        else:
            F_q[q].append((np.mean(np.array(F_s_scale) ** (q / 2))) ** (1 / q))

'''

'''
# Convert results to arrays for plotting
scales = np.array(scales)
for q in q_values:
    F_q[q] = np.array(F_q[q])


plt.figure(figsize=(8, 6))
colors = ["red", "blue", "black"]

for i, q in enumerate(q_values):
    plt.plot(np.log2(scales), np.log2(F_q[q]), label=f"q={q}", color=colors[i % len(colors)])

# Set x-axis ticks with scale values
selected_scales = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]  
plt.xticks(ticks=np.log2(selected_scales), labels=selected_scales)

plt.ylabel("log2(F(q))")
plt.legend()
plt.title("USA")
plt.show()
'''


'''
#calculating husrt exponent

hurst_exponents = {}

for q in q_values:
    log_scales = np.log2(scales)
    log_Fq = np.log2(F_q[q])

    # Perform linear fit: log(F_q) = h(q) * log(s) + C
    slope, intercept = np.polyfit(log_scales, log_Fq, 1)
    
    # Store h(q) value
    hurst_exponents[q] = slope  

# Convert to DataFrame
hurst_df = pd.DataFrame({"q": list(hurst_exponents.keys()), "h(q)": list(hurst_exponents.values())})

# Save to CSV
#hurst_df.to_csv("/home/student/Coding/Database/China_Hq.csv", index=False)



# Compute τ(q)
tau_q = {q: q * h_q - 1 for q, h_q in hurst_exponents.items()}

# Convert to DataFrame
combined_df = pd.DataFrame({
    "q": list(hurst_exponents.keys()), 
    "h(q)": list(hurst_exponents.values()), 
    "τ(q)": list(tau_q.values())
})

# Save to CSV
#combined_df.to_csv("/home/student/Coding/Database/SA_tq.csv", index=False)


# Calculate α 
q_values = sorted(hurst_exponents.keys())
tau_values = [q * hurst_exponents[q] - 1 for q in q_values] 

# Compute α(q) using central difference method
alpha_values = np.gradient(tau_values, q_values)  # Finite difference approximation

# Convert to DataFrame
alpha_df = pd.DataFrame({
    "q": q_values,
    "h(q)": [hurst_exponents[q] for q in q_values],
    "τ(q)": tau_values,
    "α(q)": alpha_values
})

# Save to CSV
# alpha_df.to_csv("/home/student/Coding/Database/Russia_alpha.csv", index=False)


# f(α) using the formula f(α) = q * α(q) - τ(q)
f_alpha = {q: q * alpha - tau_q[q] for q, alpha in zip(q_values, alpha_values)}

# Convert to DataFrame
f_alpha_df = pd.DataFrame({
    "q": q_values,
    "h(q)": [hurst_exponents[q] for q in q_values],
    "τ(q)": [tau_q[q] for q in q_values],
    "α(q)": alpha_values,
    "f(α)": [f_alpha[q] for q in q_values]
})

# Save to CSV
f_alpha_df.to_csv("/home/student/Coding/Database/USA_f(α).csv", index=False)

'''


'''
# Check polynomial fit on a sample segment
s = 512 
v = 5  

segment = profile[v * s : (v + 1) * s]
x = np.arange(s)

poly_coeffs = np.polyfit(x, segment, deg=2)  # 2nd-degree polynomial fit
poly_trend = np.polyval(poly_coeffs, x)

plt.figure(figsize=(8, 4))
plt.plot(x, segment, label="Original Segment", marker="o")
plt.plot(x, poly_trend, label="Fitted Polynomial Trend", linestyle="--", color="r")
plt.xlabel("Time index within segment")
plt.ylabel("Amplitude")
plt.title("Polynomial Fit on Sample Segment (s=128)")
plt.legend()
plt.show()

# Fit a linear model
log_s = np.log(scales)
log_Fs = np.log(F_s)

slope, intercept = np.polyfit(log_s, log_Fs, 1)  # Linear regression

print(f"Estimated Hurst Exponent (h): {slope:.4f}")
'''




'''
#Yearwise Hurst Exponent

df = datasets["SA"]
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year  # Extract year column

scales = [8, 16, 32, 64, 128, 256, 512]  
q = 2  

hurst_yearwise = {}

# Loop over years
for selected_year in range(2012, 2025):
    df_year = df[df["Year"] == selected_year]  # Filter data for the year
    
    if df_year.empty:  # Skip if no data for the year
        continue

    profile = df_year["Close"].values

    F_s_scale = []

    for s in scales:
        num_segments = len(profile) // s
        if num_segments < 1:  # Skip invalid scales
            continue

        F_s = []

        for v in range(num_segments):
            segment = profile[v * s : (v + 1) * s]
            x = np.arange(s)

            poly_coeffs = np.polyfit(x, segment, deg=2)
            poly_trend = np.polyval(poly_coeffs, x)

            fluctuation = (segment - poly_trend) ** 2
            F_s.append(np.mean(fluctuation))

        F_q_s = (np.mean(np.array(F_s) ** (q / 2))) ** (1 / q)
        
        if np.isfinite(F_q_s) and F_q_s > 0:  # Ensure valid values
            F_s_scale.append(F_q_s)

    # Compute h(1) using linear regression
    if len(F_s_scale) > 1:
        log_scales = np.log2(scales[:len(F_s_scale)])  
        log_Fq = np.log2(F_s_scale)

        slope, intercept = np.polyfit(log_scales, log_Fq, 1)
        hurst_yearwise[selected_year] = slope  # Store Hurst exponent h(1)

# Convert results to lists for plotting
years = list(hurst_yearwise.keys())
h_q_values = list(hurst_yearwise.values())



# Save to CSV file
hurst_df = pd.DataFrame({"Year": years, "h(1)": h_q_values})
hurst_df.to_csv("/home/student/Study/Country/Yearwise_H/SA_2.csv", index=False)
'''

'''
#Plot h(1) vs Year
plt.figure(figsize=(8, 6))
plt.plot(years, h_q_values, marker="o", linestyle="-", color="blue", label="Hurst Exponent (h(2))")
plt.xlabel("Year")
plt.ylabel("h(2)")
plt.title("Yearwise Hurst Exponent (q=2) for South Africa")
plt.grid(True)
plt.legend()
plt.show()
'''


#Year wise multifractal spectrum

df = datasets["SA"]
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

scales = [8, 16, 32, 64, 128, 256, 512]
q_values = np.arange(-5, 5.1, 0.2)

hurst_yearwise = {q: {} for q in q_values}

for selected_year in range(2010, 2025):
    df_year = df[df["Year"] == selected_year]
    if df_year.empty:
        continue

    profile = df_year["Close"].values

    for q in q_values:
        F_s_scale = []

        for s in scales:
            num_segments = len(profile) // s
            if num_segments < 1:
                continue

            F_s = []

            for v in range(num_segments):
                segment = profile[v * s : (v + 1) * s]
                x = np.arange(s)

                poly_coeffs = np.polyfit(x, segment, deg=2)
                poly_trend = np.polyval(poly_coeffs, x)

                fluctuation = (segment - poly_trend) ** 2
                F_s.append(np.mean(fluctuation))

            F_s = np.array(F_s)

            # Compute F_q(s)
            if q == 0:
                F_q_s = np.exp(0.5 * np.mean(np.log(F_s[F_s > 0])))  # log averaging
            else:
                F_q_s = (np.mean(F_s ** (q / 2))) ** (1 / q)

            if np.isfinite(F_q_s) and F_q_s > 0:
                F_s_scale.append(F_q_s)

        if len(F_s_scale) > 1:
            log_scales = np.log2(scales[:len(F_s_scale)])
            log_Fq = np.log2(F_s_scale)
            slope, _ = np.polyfit(log_scales, log_Fq, 1)
            hurst_yearwise[q][selected_year] = slope

# Convert to DataFrame
hurst_df = pd.DataFrame(hurst_yearwise).T  # q as rows
hurst_df.columns.name = "Year"
hurst_df.index.name = "q"

# # Save CSV
# hurst_df.to_csv("/home/student/Study/Country/Yearwise_H/USA_qrange.csv")

plt.figure(figsize=(10, 6))

offset_step = 0.1  # how much to shift each year upward
i = 0  # index for offset

# Loop through years
for year in sorted(hurst_df.columns):
    hq = hurst_df[year].dropna().values
    qs = hurst_df[year].dropna().index.astype(float)

    if len(hq) < 5:
        continue

    tau_q = qs * hq - 1
    alpha = np.gradient(tau_q, qs)
    f_alpha = qs * alpha - tau_q

    # Apply vertical offset
    f_alpha_shifted = f_alpha + i * offset_step

    plt.plot(alpha, f_alpha_shifted, label=str(year))
    i += 1  # increase offset for next year

# Plot formatting
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$f(\alpha)$ (shifted)")
plt.title("Yearwise Multifractal Spectrum — South Africa")
plt.legend(fontsize='x-small', ncol=3, loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()