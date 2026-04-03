# Milestone 3: Interim Status Report

## 1. Task Updates and Artifacts
### Data Acquisition ✅ Complete
All raw datasets have been successfully collected and stored in `data/raw/`:

- **Traditional Stats**: Collected via [`scripts/fetch_player_stats.py`](scripts/fetch_player_stats.py) using `nba_api` → [`data/raw/player_stats_traditional.csv`](data/raw/player_stats_traditional.csv)
- **Advanced Stats**: Collected via [`scripts/fetch_player_stats.py`](scripts/fetch_player_stats.py) using `nba_api` → [`data/raw/player_stats_advanced.csv`](data/raw/player_stats_advanced.csv)
- **Player Salaries**: Scraped via [`scripts/fetch_salaries.py`](scripts/fetch_salaries.py) from Basketball-Reference → [`data/raw/player_salaries.csv`](data/raw/player_salaries.csv)
- **Team Standings**: Scraped via [`scripts/fetch_team_standings.py`](scripts/fetch_team_standings.py) from Basketball-Reference → [`data/raw/team_standings.csv`](data/raw/team_standings.csv)

### Data Integration 🔄 In Progress
SQL/Pandas joins across datasets are planned. Entity resolution for player name inconsistencies is being addressed.

### Data Cleaning 🔄 In Progress
Initial inspection identified issues including accented characters in player names, salary formatting ($), and missing salary entries for two-way contract players.

### Workflow Automation ⬜ Not Started
A master automation script (main.py or Snakemake) will be developed to link all steps end-to-end.
## 2. Updated Project Timeline
[Insert your updated table with a 'Status' column.]

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
(Whatever TA or Professor said about it)

## 4. Challenges and Resolutions
[Mention API limits, name cleaning, or SQL join issues.]

## 5. Individual Contribution Summaries
### Summary: Colin Cosillo
[Colin's text here]

### Summary: Daniel Kang
[Daniel's text here]
