import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# Function to scrape real-time cryptocurrency prices
def scrape_crypto_prices():
    url = "https://coinmarketcap.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Finding the first few cryptocurrency data (e.g., Bitcoin, Ethereum)
    cryptos = []
    rows = soup.select("tr.cmc-table-row")[:5]  # Adjust to get more rows if needed

    for row in rows:
        name = row.select_one("td.cmc-table__cell--sort-by__name").text.strip()
        price = row.select_one("td.cmc-table__cell--sort-by__price").text.strip()
        cryptos.append({"name": name, "price": price})

    # Append timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for crypto in cryptos:
        crypto["timestamp"] = timestamp

    return cryptos

# Function to save data to CSV
def save_to_csv(data, filename="crypto_prices.csv"):
    if not os.path.isfile(filename):
        pd.DataFrame(data).to_csv(filename, index=False)
    else:
        pd.DataFrame(data).to_csv(filename, mode="a", header=False, index=False)

# Scrape data and save to CSV
crypto_data = scrape_crypto_prices()
save_to_csv(crypto_data)

print("Data scraped and saved successfully.")
