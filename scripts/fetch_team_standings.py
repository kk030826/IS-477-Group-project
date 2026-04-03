"""
fetch_team_standings.py
Scrapes 2024-25 NBA team standings from Basketball-Reference
and saves to data/raw/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
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

soup = BeautifulSoup(resp.text, "html.parser")

# Get Eastern and Western conference tables separately
east_table = soup.find("table", {"id": "divs_standings_E"})
west_table = soup.find("table", {"id": "divs_standings_W"})

df_east = pd.read_html(io.StringIO(str(east_table)))[0]
df_east["conference"] = "East"

df_west = pd.read_html(io.StringIO(str(west_table)))[0]
df_west["conference"] = "West"

# Rename first column to team_name
df_east.columns = ["team_name"] + list(df_east.columns[1:])
df_west.columns = ["team_name"] + list(df_west.columns[1:])

# Remove division header rows (they don't have W/L data)
df_east = df_east[pd.to_numeric(df_east["W"], errors="coerce").notna()]
df_west = df_west[pd.to_numeric(df_west["W"], errors="coerce").notna()]

df = pd.concat([df_east, df_west], ignore_index=True)

df.to_csv("data/raw/team_standings.csv", index=False)
print(f"  Saved {len(df)} teams -> data/raw/team_standings.csv")
print(df[["team_name", "W", "L", "W/L%", "conference"]].to_string())
