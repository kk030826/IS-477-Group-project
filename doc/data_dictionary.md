# Data Dictionary: Integrated NBA Dataset

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `player_name` | String | Standardized name of the NBA player (normalized for entity resolution). |
| `team_abbrev` | String | Three-letter abbreviation of the player's 2024-25 team. |
| `salary_2025_26`| Float | Projected annual base salary for the 2025-26 season in USD. |
| `total_guaranteed`| Float | Total remaining guaranteed money in the player's current contract. |
| `AGE` | Float | Player's age at the start of the 2024-25 season. |
| `GP` | Integer | Games played in the most recent full season. |
| `TS_PCT` | Float | True Shooting Percentage: A measure of shooting efficiency (FT and 3PT included). |
| `PIE` | Float | Player Impact Estimate: A holistic measure of a player's statistical contribution. |
| `USG_PCT` | Float | Usage Percentage: An estimate of the percentage of team plays used by a player. |
| `PTS` | Float | Average points scored per game. |
| `team_wins` | Integer | Total wins recorded by the player's team. |
| `team_win_pct` | Float | The winning percentage of the team (Team Wins / Total Games). |
