"""
fetch_player_stats.py
Collects NBA player traditional + advanced stats for 2024-25 season
via nba_api and saves to data/raw/
"""

import time
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import os

os.makedirs("data/raw", exist_ok=True)

print("Fetching traditional stats...")
time.sleep(1)

trad = leaguedashplayerstats.LeagueDashPlayerStats(
    season="2024-25",
    per_mode_detailed="PerGame",
    measure_type_detailed_defense="Base"
)
df_trad = trad.get_data_frames()[0]
df_trad.to_csv("data/raw/player_stats_traditional.csv", index=False)
print(f"  Saved {len(df_trad)} players -> data/raw/player_stats_traditional.csv")

time.sleep(2)  # rate limit

print("Fetching advanced stats...")
adv = leaguedashplayerstats.LeagueDashPlayerStats(
    season="2024-25",
    per_mode_detailed="PerGame",
    measure_type_detailed_defense="Advanced"
)
df_adv = adv.get_data_frames()[0]
df_adv.to_csv("data/raw/player_stats_advanced.csv", index=False)
print(f"  Saved {len(df_adv)} players -> data/raw/player_stats_advanced.csv")

print("Done.")
