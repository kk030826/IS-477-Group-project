# Milestone 2: Project Plan

### Overview
The primary objective of this project is to evaluate the correlation between National Basketball Association (NBA) player compensation and on-court productivity. This evaluation will be done by integrating individual performance metrics with contractual salary and team performance data. We will focus on identifying "undervalued" players that have statistical contributions that exceed their market valuation. We will analyze the correlation of advanced metrics, traditional "box score" statistics, and team performance with salary to see what goes into modern NBA salary decisions.

To achieve this, we will execute an end-to-end data pipeline with the following main steps:

**Acquisition:** Harvesting performance data from the official NBA website and utilizing the nba_api, scraping advanced player metrics and historical financial records from reputable sources like Basketball-Reference, and getting team standings from official NBA archives.

**Integration:** Utilizing Python to resolve entity discrepancies for data cleaning and consistency purposes and performing multi-key joins across player, season, and team identifiers using SQL.

**Analysis:** Correlate salary levels with performance tiers, identifying outliers who represent high-value player contracts and answering our research questions.

**Validation:** Documenting our workflow through a reproducible GitHub repository, including data cleaning and integration steps for transparency and automated scripts for data tracking to ensure our project is repeatable and a clear record of how the data was handled.

### Team



### Research Questions
Primary Research Question: To what extent do advanced efficiency metrics (like PER and Win Shares) predict a player’s salary compared to traditional "box score" stats like points per game?

Analytical Question: Who are "under-valued" players whose statistical contributions significantly exceed their contractual cost?

### Datasets: Identification and Description
To analyze the relationship between player performance and market value, our team will integrate the following three datasets:

**NBA Player Statistics (Performance Data)**

Description: Contains seasonal box-score metrics for individual players.

Key Attributes: Player_Name (String), Season (Integer), Points_Per_Game (Float), True_Shooting_Percentage (Float), and PER (Player Efficiency Rating).

Source: Professional basketball reference sites (e.g., Basketball-Reference).

**NBA Player Salaries (Financial Data)**

Description: Historical data of annual salaries and contract lengths for NBA players.

Key Attributes: Player_Name (String), Season (Integer), Salary (Numeric), Team_Affiliation (String).

Source: Financial tracking databases (e.g., HoopsHype or Spotrac).

**NBA Team Standings (Success Metrics)**

Description: Data regarding team-level success to determine if team winning percentage correlates with individual overpayment.

Key Attributes: Team_Name (String), Win_Loss_Percentage (Float), Playoff_Appearance (Boolean).

Source: Official NBA historical standings.

### Timeline

### Constraints

### Gaps

### Data Lifecycle and Storage Strategy

As the lead for data architecture, I will oversee the following lifecycle:

Ingestion: Data will be collected via Python-based web scraping and API calls. Raw files will be initially stored in a data/raw/ directory in .csv format to preserve the original provenance.

Processing & Cleaning: * Schema Standardization: Ensuring all column names follow snake_case and data types (e.g., converting salary strings like "$40M" to float values) are consistent.

Entity Resolution: Standardizing player names (e.g., "Luka Doncic" vs "Luka Dončić") to ensure seamless joining across different sources.

Storage & Organization: * Processed data will be stored in data/processed/ as a master integrated file.

For the GitHub repository, I will implement a clear directory structure to separate the document schema from the actual analysis scripts, ensuring the project remains scalable and organized.
