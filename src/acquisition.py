import os
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import time

# 1. Create directory for raw data if it doesn't exist
os.makedirs('../data/raw', exist_ok=True)

print("Fetching player statistics from NBA API...")

try:
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season='2023-24',
        per_mode_detailed='PerGame',
        season_type_all_star='Regular Season'
    )
    
    df = stats.get_data_frames()[0]
    
    file_path = '../data/raw/nba_stats_2023_24.csv'
    df.to_csv(file_path, index=False)
    
    print(f"Success! Data has been saved to: {file_path}")
    print(f"Total players fetched: {len(df)}")

except Exception as e:
    print(f"Error occurred: {e}")
    print("Tip: Check your internet connection or wait a moment (Rate Limit).")
