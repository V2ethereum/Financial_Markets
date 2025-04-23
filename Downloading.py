import yfinance as yf

'''# Define indices for BRICS countries and MSCI Emerging Markets (MXEF)
indices = {
    "Brazil": "^BVSP",        # IBOVESPA
    "Russia": "IMOEX.ME",     # MOEX Russia
    "India": "^NSEI",         # NIFTY 50
    "China": "000001.SS",     # SSE Composite
    "South Africa": "^J203.JO",  # FTSE/JSE All Share
    "MXEF": "^MXEF"           # MSCI Emerging Markets Index
}

# Define start and end dates
start_date = "2018-01-01"
end_date = "2022-12-31"

# Download data for each index and save to CSV
for country, ticker in indices.items():
    print(f"Downloading data for {country} ({ticker})...")
    data = yf.download(ticker, start=start_date, end=end_date)
    data.to_csv(f"{country}_data.csv")  # Save to CSV file

print("✅ All data downloaded successfully!")'''



Brazil = yf.download('^BVSP', start="1994-01-03", end="2025-04-01")
Brazil.to_csv('Brazil_data.csv')

India = yf.download('^NSEI', start = "1998-01-01", end = "2025-04-01")
India.to_csv('India_data.csv')

Russia =  yf.download('IMOEX.ME', start = "1997-09-22", end = "2025-04-01")
Russia.to_csv('Russia_data.csv')

China = yf.download('000001.SS', start = "1990-12-19", end = "2025-04-01")
China.to_csv('China_data.csv')

SA = yf.download('^J203.JO', start = "1995-07-02", end = "2025-04-01")
SA.to_csv('SA_data.csv')


print("ALL data downloaded successfully!")


