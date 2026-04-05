# Milestone 3: Interim Status Report

## 1. Task Updates and Artifacts
### Data Acquisition 
All raw datasets have been successfully collected and stored in `data/raw/`:

- **Traditional Stats**: Collected via [`scripts/fetch_player_stats.py`](scripts/fetch_player_stats.py) using `nba_api` → [`data/raw/player_stats_traditional.csv`](data/raw/player_stats_traditional.csv)
- **Advanced Stats**: Collected via [`scripts/fetch_player_stats.py`](scripts/fetch_player_stats.py) using `nba_api` → [`data/raw/player_stats_advanced.csv`](data/raw/player_stats_advanced.csv)
- **Player Salaries**: Scraped via [`scripts/fetch_salaries.py`](scripts/fetch_salaries.py) from Basketball-Reference → [`data/raw/player_salaries.csv`](data/raw/player_salaries.csv)
- **Team Standings**: Scraped via [`scripts/fetch_team_standings.py`](scripts/fetch_team_standings.py) from Basketball-Reference → [`data/raw/team_standings.csv`](data/raw/team_standings.csv)

### Data Integration 
## Integration Artifacts

* **Master Integration Script:** [`scripts/integrate_nba_data.py`](scripts/integrate_nba_data.py)
    * *Description:* This Python script automates the end-to-end integration process. It handles entity resolution for player names, maps team abbreviations to full names, initializes the SQLite environment, and executes the final multi-key SQL join.
* **Relational Database Artifact:** [`data/processed/nba_project.db`](data/processed/nba_project.db)
    * *Description:* A localized SQLite database file containing the normalized relational tables (`salaries`, `stats_adv`, `stats_trad`, `standings`, and `team_map`). This serves as the primary storage layer for our curated data.
* **Integrated Master Dataset:** [`data/processed/integrated_nba_data.csv`](data/processed/integrated_nba_data.csv)
    * *Description:* The final output of the integration pipeline. This CSV contains 14 merged attributes across all four data sources, providing the clean "analytical view" required for our upcoming correlation analysis.
* **Integration Run Notebook:** [`Integration_Run.ipynb`](Integration_Run.ipynb)
    * *Description:* The notebook that runs the master integration script

### Data Cleaning
The following issues were identified and resolved using `scripts/clean_data.py`:

- **Player name encoding**: Fixed accented characters (e.g., "Nikola JokiÄ" → "Nikola Jokić") using latin1/utf-8 re-encoding
- **Salary formatting**: Removed `$` symbols and commas from salary columns and converted to float (e.g., "$55,224,526" → 55224526.0)
- **Shifted columns**: Fixed misaligned columns in salary data where rank numbers appeared in the player_name column
- **Minimum minutes filter**: Removed players with fewer than 10 minutes per game from stats datasets (569 → 458 players)
- **Team name formatting**: Removed playoff asterisks from team names (e.g., "Cleveland Cavaliers*" → "Cleveland Cavaliers")
- **Duplicate entries**: Removed duplicate player rows by keeping the entry with highest minutes played

Cleaned files saved to `data/processed/`:
- [`data/processed/player_salaries_clean.csv`](data/processed/player_salaries_clean.csv)
- [`data/processed/player_stats_traditional_clean.csv`](data/processed/player_stats_traditional_clean.csv)
- [`data/processed/player_stats_advanced_clean.csv`](data/processed/player_stats_advanced_clean.csv)
- [`data/processed/team_standings_clean.csv`](data/processed/team_standings_clean.csv)
### Workflow Automation
A master automation script (main.py or Snakemake) will be developed to link all steps end-to-end.

* **Workflow Diagram:** [`doc/workflow_diagram.png`](doc/workflow_diagram.png) 
    * *Description:* A visual representation of our data lifecycle, illustrating the flow from raw acquisition to the SQL-integrated master file.
 
## 2. Updated Project Timeline

The following table outlines our progress as of April 3, 2026. We have successfully transitioned from the data acquisition phase to the integration phase, and are currently on track to begin the final analysis.

| Phase | Task | Status | Deadline | Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **Milestone 2** | Project Plan Submission | **Complete** | March 8, 2026 | Lead Strategist |
| **Acquisition** | Raw Performance Data Harvesting | **Complete** | March 15, 2026 | Lead Architect |
| **Acquisition** | Salary Web Scraping (HoopsHype) | **Complete** | March 18, 2026 | Lead Architect |
| **Integration** | SQL Database & Schema Setup | **Complete** | March 22, 2026 | Lead Strategist |
| **Integration** | Entity Resolution (Name Normalization) | **Complete** | March 25, 2026 | Lead Strategist |
| **Integration** | Multi-Source SQL Table Merging | **Complete** | April 1, 2026 | Lead Strategist |
| **Milestone 3** | Interim Status Report | **In Progress** | April 5, 2026 | Both |
| **Analysis** | Efficiency vs. Salary Value Modeling | Not Started | April 15, 2026 | Both |
| **Analysis** | Data Visualization (Seaborn/Matplotlib) | Not Started | April 22, 2026 | Lead Strategist |
| **Finalization** | Workflow Automation (Snakemake/Main script) | Not Started | April 29, 2026 | Lead Architect |
| **Finalization** | Final Report & Release | Not Started | May 6, 2026 | Both |

## 3. Changes to Project Plan

### Data Source Change: HoopsHype → Basketball-Reference
Originally, our project plan specified HoopsHype as the primary source 
for NBA player salary data. During implementation, HoopsHype returned 
a 404 HTTP error, indicating that the page structure has changed or 
that automated scraping is blocked. As an alternative, we switched to 
Basketball-Reference, which provides equivalent salary and contract 
data for all NBA players. Basketball-Reference is a more established 
academic source with a clear robots.txt policy that permits reasonable 
scraping for non-commercial use.

### Dataset Scope Clarification
Our original plan described three datasets. Upon implementation, we 
clarified that the nba_api produces two separate CSV files — one for 
traditional box score stats and one for advanced metrics. These are 
treated as two complementary datasets from the same API source, and 
will be merged on player ID before integration with the salary data.

### No Changes to Research Questions
Our core research questions remain unchanged:
- To what extent do advanced efficiency metrics predict a player's 
  salary compared to traditional stats?
- Can we identify "undervalued" players whose contributions 
  significantly exceed their contractual costs?

### Feedback from Milestone 2
In response to TA feedback requesting clarification on dataset 
licensing and data format requirements, we provide the following:

**Licensing:**
- **nba_api**: Interfaces with NBA.com's publicly available statistics 
  endpoint. Used strictly for non-commercial, educational research 
  purposes in compliance with NBA.com's Terms of Use.
- **Basketball-Reference (Stats & Salaries)**: Data is available for 
  personal and non-commercial use per their Terms of Use. Our scraping 
  frequency complies with their `robots.txt` policy.

**Different Data Formats/Access Methods:**
Our datasets satisfy the requirement for different access methods:
- **nba_api** (API-based access): Player traditional and advanced stats 
  are retrieved programmatically via a Python API wrapper, returning 
  structured JSON data that is converted to CSV.
- **Web Scraping** (HTTP-based access): Salary and team standings data 
  are collected via `requests` and `BeautifulSoup` by parsing raw HTML 
  tables from Basketball-Reference.

These two distinct acquisition methods demonstrate different data 
collection techniques as required by the project guidelines.

## 4. Challenges and Resolutions

### 1. Entity Resolution (Name Normalization)
**Problem:** During the initial join between our `player_salaries_clean.csv` and `player_stats_advanced_clean.csv`, we observed a significant drop in the number of matched records (a "data loss" of approximately 18%). Upon investigation, we found that the datasets were inconsistent in their handling of international characters and suffixes. For example, the NBA API data uses UTF-8 characters like "ć" in *Nikola Jokić*, whereas financial databases often normalize these to "c." Furthermore, inconsistencies in suffixes (e.g., "Kelly Oubre Jr." vs. "Kelly Oubre") prevented standard SQL joins from recognizing them as the same entity.

**Resolution:** To resolve this, I developed a robust `normalize_name` function in Python. This function performs three critical steps:
1. **Character Mapping:** It uses a dictionary to manually map accented characters to their standard English equivalents.
2. **Regex Stripping:** It uses regular expressions to remove punctuation and extra whitespace, effectively treating "P.J. Tucker" and "PJ Tucker" as identical keys.
3. **Join-Key Generation:** Instead of joining on the raw `player_name`, we created a hidden `norm_name` column in every SQLite table. By joining on this normalized key, we recovered nearly all of the missing records, raising our match rate to over 98%.

### 2. Multi-Source Integration (Team Abbreviations and Full Names)
**Problem:** A major goal of our project is to correlate individual value with team success. However, our team standings dataset from Basketball-Reference uses full geographic names (e.g., "Philadelphia 76ers"), while the player statistics from the NBA API use three-letter abbreviations (e.g., "PHI"). Because there is no "Natural Join" possible between these two formats, we faced a "siloed data" problem where team-level metrics could not be attached to player-level salaries.

**Resolution:** I addressed this by designing a **Relational Mapping Table** within our SQLite database. 
* I created a `team_map` table that explicitly links every NBA abbreviation to its corresponding full name. 
* In the final integration script, I implemented a "Double Join" logic: joining the Player to the Team Abbreviation, then joining that Abbreviation to the Mapping Table, and finally joining the Mapping Table to the Standings. 
This multi-step SQL integration ensures that our final master dataset includes team winning percentages for every player, allowing us to answer our core research questions regarding the correlation between winning and "overpayment."

### 3. File Path Stability
**Problem:** As we moved from simple CSV files to a structured database, we encountered "File Not Found" errors when running the scripts on different machines. This happened because Python's relative file paths depend on where the terminal is opened, which threatened the "one-click reproducibility" required for this project.

**Resolution:** I updated the integration script to use more defensive programming techniques. By utilizing the `os` and `pathlib` libraries, I added logic to automatically detect the project root and create necessary directories (like `data/processed/`) if they do not exist. This ensures that when our Lead Architect runs the automation script, the SQL database is initialized and the master CSV is exported to the correct folder regardless of the local environment setup.

## 5. Individual Contribution Summaries
### Summary: Colin Cosillo
I took the lead on the data integration phase. I developed a Python-based SQL pipeline that loads four disparate CSV datasets into a relational SQLite database. I implemented an Entity Resolution function to standardize player names across sources and created a relational 'Team Map' to link player-level statistics with team-level standings. I also updated the project timeline, made the workflow diagram, and documented our technical challenges regarding name-matching discrepancies, multi-source integration, and File Path Stability.

### Summary: Daniel Kang
I was responsible for the entire data acquisition pipeline. I developed  and executed all three data collection scripts in the `scripts/` directory: `fetch_player_stats.py` (nba_api), `fetch_salaries.py` (Basketball-Reference scraping), and `fetch_team_standings.py` (Basketball-Reference scraping). I also set up the repository directory structure (`data/raw/`, `data/processed/`, `scripts/`), debugged `nba_api` parameter errors caused by a library version change, and resolved a HoopsHype scraping failure by switching to Basketball-Reference. Additionally, I developed `scripts/clean_data.py` to address data quality issues including player name encoding errors, salary formatting, shifted columns, and team name inconsistencies across all four datasets.
