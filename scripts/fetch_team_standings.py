"""
fetch_team_standings.py
Scrapes 2024-25 NBA team standings + advanced metrics from Basketball-Reference
and saves to data/raw/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

URL = "https://www.basketball-reference.com/leagues/NBA_2025_standings.html"

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

# pandas can read HTML tables directly
tables = pd.read_html(resp.text)

# Eastern Conference = tables[0], Western Conference = tables[1]
df_east = tables[0].copy()
df_east["conference"] = "East"

df_west = tables[1].copy()
df_west["conference"] = "West"

df = pd.concat([df_east, df_west], ignore_index=True)

# rename team column (varies by year)
df.rename(columns={df.columns[0]: "team_name"}, inplace=True)

# clean up multi-level headers if any
df.columns = [str(c).strip() for c in df.columns]

df.to_csv("data/raw/team_standings.csv", index=False)
print(f"  Saved {len(df)} teams -> data/raw/team_standings.csv")
print(df.head())
