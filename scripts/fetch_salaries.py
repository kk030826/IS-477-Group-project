"""
fetch_salaries.py
Scrapes 2024-25 NBA player salary data from Basketball-Reference
and saves to data/raw/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import os

os.makedirs("data/raw", exist_ok=True)

URL = "https://www.basketball-reference.com/contracts/players.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

print(f"Scraping: {URL}")
resp = requests.get(URL, headers=headers)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", {"id": "player-contracts"})

df = pd.read_html(io.StringIO(str(table)))[0]

# flatten multi-level columns if needed
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [' '.join(col).strip() for col in df.columns]

df.columns = df.columns.str.strip()
print("Columns:", df.columns.tolist())

# rename first two columns
df = df.rename(columns={df.columns[0]: "player_name", df.columns[1]: "team"})

# drop repeated header rows
df = df[df["player_name"] != "Player"]
df = df.dropna(subset=["player_name"])

df.to_csv("data/raw/player_salaries.csv", index=False)
print(f"  Saved {len(df)} players -> data/raw/player_salaries.csv")
print(df.head())
