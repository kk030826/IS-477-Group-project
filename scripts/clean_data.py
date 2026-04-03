"""
clean_data.py
Cleans and standardizes all raw datasets before integration.
Saves cleaned files to data/processed/
"""

import pandas as pd
import os

os.makedirs("data/processed", exist_ok=True)

# ── 1. SALARY DATA ──────────────────────────────────────────────
print("=== Cleaning Salary Data ===")
sal = pd.read_csv("data/raw/player_salaries.csv")
print("Before:", sal.shape)
print(sal.head(3))

# Fix shifted columns: rank is in col0, player_name is in col1, team in col2
sal.columns = ["rank", "player_name", "team",
               "salary_2025_26", "salary_2026_27", "salary_2027_28",
               "salary_2028_29", "salary_2029_30", "salary_2030_31",
               "guaranteed"]

# Drop rank column
sal = sal.drop(columns=["rank"])

# Drop repeated header rows
sal = sal[sal["player_name"] != "Player"]
sal = sal.dropna(subset=["player_name"])

# Fix encoding issues (e.g., JokiÄ -> Jokić)
sal["player_name"] = sal["player_name"].str.encode("latin1").str.decode("utf-8", errors="replace")

# Clean salary columns: remove $ and commas, convert to float
for col in ["salary_2025_26", "salary_2026_27", "salary_2027_28",
            "salary_2028_29", "salary_2029_30", "salary_2030_31", "guaranteed"]:
    sal[col] = sal[col].astype(str).str.replace(r"[$,]", "", regex=True)
    sal[col] = pd.to_numeric(sal[col], errors="coerce")

# Strip whitespace from player names
sal["player_name"] = sal["player_name"].str.strip()

print("After:", sal.shape)
print(sal.head(3))
sal.to_csv("data/processed/player_salaries_clean.csv", index=False)
print("Saved -> data/processed/player_salaries_clean.csv\n")


# ── 2. TRADITIONAL STATS ────────────────────────────────────────
print("=== Cleaning Traditional Stats ===")
trad = pd.read_csv("data/raw/player_stats_traditional.csv")
print("Before:", trad.shape)

# Standardize player name column
trad = trad.rename(columns={"PLAYER_NAME": "player_name"})

# Drop duplicate player entries (keep highest MIN)
trad = trad.sort_values("MIN", ascending=False).drop_duplicates(subset=["player_name"])

# Strip whitespace
trad["player_name"] = trad["player_name"].str.strip()

# Filter: minimum 10 minutes played per game
trad = trad[trad["MIN"] >= 10]

print("After:", trad.shape)
trad.to_csv("data/processed/player_stats_traditional_clean.csv", index=False)
print("Saved -> data/processed/player_stats_traditional_clean.csv\n")


# ── 3. ADVANCED STATS ───────────────────────────────────────────
print("=== Cleaning Advanced Stats ===")
adv = pd.read_csv("data/raw/player_stats_advanced.csv")
print("Before:", adv.shape)

adv = adv.rename(columns={"PLAYER_NAME": "player_name"})
adv = adv.sort_values("MIN", ascending=False).drop_duplicates(subset=["player_name"])
adv["player_name"] = adv["player_name"].str.strip()
adv = adv[adv["MIN"] >= 10]

print("After:", adv.shape)
adv.to_csv("data/processed/player_stats_advanced_clean.csv", index=False)
print("Saved -> data/processed/player_stats_advanced_clean.csv\n")


# ── 4. TEAM STANDINGS ───────────────────────────────────────────
print("=== Cleaning Team Standings ===")
stand = pd.read_csv("data/raw/team_standings.csv")
print("Before:", stand.shape)

# Remove asterisks from team names (e.g., "Cleveland Cavaliers*" -> "Cleveland Cavaliers")
stand["team_name"] = stand["team_name"].str.replace("*", "", regex=False).str.strip()

# Drop rows where team_name is NaN or "Western Conference"/"Eastern Conference"
stand = stand[~stand["team_name"].isin(["Eastern Conference", "Western Conference"])]
stand = stand.dropna(subset=["team_name"])

print("After:", stand.shape)
stand.to_csv("data/processed/team_standings_clean.csv", index=False)
print("Saved -> data/processed/team_standings_clean.csv\n")

print("=== All cleaning complete! ===")
