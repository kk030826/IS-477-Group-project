import pandas as pd
import sqlite3
import re
import os

# 1. Entity Resolution: Normalize Player Names
def normalize_name(name):
    if pd.isna(name):
        return None
    # Convert to lowercase and strip whitespace
    name = str(name).lower().strip()
    # Mapping for common NBA special characters to standard English characters
    mapping = {
        'ć': 'c', 'č': 'c', 'š': 's', 'ž': 'z', 'đ': 'd',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ý': 'y', 'ö': 'o'
    }
    for char, repl in mapping.items():
        name = name.replace(char, repl)
    # Remove punctuation (handles "P.J. Tucker" vs "PJ Tucker")
    name = re.sub(r'[^a-z0-9\s]', '', name)
    return name

def main():
    if os.path.exists('data'):
        print("The 'data' folder exists!")
    else:
        print("The 'data' folder is missing.")
    # Load the 4 cleaned CSV datasets
    # Note: Ensure these files are in the same directory or provide full paths
    salaries = pd.read_csv('data/processed/player_salaries_clean.csv')
    stats_adv = pd.read_csv('data/processed/player_stats_advanced_clean.csv')
    stats_trad = pd.read_csv('data/processed/player_stats_traditional_clean.csv')
    standings = pd.read_csv('data/processed/team_standings_clean.csv')

    # Apply Entity Resolution (Normalization) to the join keys
    salaries['norm_name'] = salaries['player_name'].apply(normalize_name)
    stats_adv['norm_name'] = stats_adv['player_name'].apply(normalize_name)
    stats_trad['norm_name'] = stats_trad['player_name'].apply(normalize_name)

    # 2. Team Mapping: Link Abbreviations to Full Team Names
    # This allows us to join the player stats (GSW) with team standings (Golden State Warriors)
    team_mapping = {
        'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BKN': 'Brooklyn Nets',
        'CHA': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers',
        'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons',
        'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers',
        'LAC': 'LA Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies',
        'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves',
        'NOP': 'New Orleans Pelicans', 'NYK': 'New York Knicks', 'OKC': 'Oklahoma City Thunder',
        'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHX': 'Phoenix Suns',
        'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs',
        'TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'
    }
    team_map_df = pd.DataFrame(list(team_mapping.items()), columns=['abbrev', 'full_name'])

    # 3. Initialize SQLite Database
    # We create a local .db file which serves as a reproducible artifact
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    conn = sqlite3.connect('data/processed/nba_project.db')
    
    # Load raw data and mapping table into SQLite as relational tables
    salaries.to_sql('salaries', conn, if_exists='replace', index=False)
    stats_adv.to_sql('stats_adv', conn, if_exists='replace', index=False)
    stats_trad.to_sql('stats_trad', conn, if_exists='replace', index=False)
    standings.to_sql('standings', conn, if_exists='replace', index=False)
    team_map_df.to_sql('team_map', conn, if_exists='replace', index=False)

    # 4. SQL JOIN Query: Integrate all 4 sources
    # We join: Advanced Stats + Traditional Stats + Salaries + Standings (via Team Map)
    query = """
    SELECT 
        s.player_name,
        s.team AS team_abbrev,
        s.salary_2025_26,
        s.guaranteed AS total_guaranteed,
        a.AGE,
        a.GP,
        a.TS_PCT,
        a.PIE,
        a.USG_PCT,
        t.PTS,
        t.REB,
        t.AST,
        st.W AS team_wins,
        st."W/L%" AS team_win_pct
    FROM salaries s
    JOIN stats_adv a ON s.norm_name = a.norm_name
    JOIN stats_trad t ON a.norm_name = t.norm_name
    JOIN team_map m ON s.team = m.abbrev
    JOIN standings st ON m.full_name = st.team_name
    """

    # Execute the query and load into a final DataFrame
    integrated_df = pd.read_sql_query(query, conn)
    conn.close()

    # 5. Export the Master Integrated Dataset
    os.makedirs('data/processed', exist_ok=True)
    integrated_df.to_csv('data/processed/integrated_nba_data.csv', index=False)
    
    print("--- Integration Complete ---")
    print(f"Total Integrated Records: {len(integrated_df)}")
    print(f"Output saved to: data/processed/integrated_nba_data.csv")
    print(f"Database artifact: data/nba_project.db")

if __name__ == "__main__":
    main()
