"""
fetch_salaries.py
Scrapes 2024-25 NBA player salary data from HoopsHype
and saves to data/raw/
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

URL = "https://hoopshype.com/salaries/players/2024-2025/"

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
table = soup.find("table", class_="hh-salaries-ranking-table")

rows = []
for tr in table.find_all("tr")[1:]:  # skip header
    cols = tr.find_all("td")
    if len(cols) >= 3:
        rank = cols[0].get_text(strip=True)
        player = cols[1].get_text(strip=True)
        salary_raw = cols[2].get_text(strip=True)
        # convert "$40,600,000" -> 40600000
        salary = int(salary_raw.replace("$", "").replace(",", "")) if salary_raw else None
        rows.append({"rank": rank, "player_name": player, "salary_2024_25": salary})

df = pd.DataFrame(rows)
df.to_csv("data/raw/player_salaries.csv", index=False)
print(f"  Saved {len(df)} players -> data/raw/player_salaries.csv")
print(df.head())
