# Milestone 2: Project Plan

## Overview
The primary objective of this project is to evaluate the correlation between National Basketball Association (NBA) player compensation and on-court productivity. This evaluation will be done by integrating individual performance metrics with contractual salary and team performance data. We will focus on identifying "undervalued" players that have statistical contributions that exceed their market valuation. We will analyze the correlation of advanced metrics, traditional "box score" statistics, and team performance with salary to see what goes into modern NBA salary decisions.

To achieve this, we will execute an end-to-end data pipeline with the following main steps:

* **Acquisition:** Harvesting performance data from the official NBA website and utilizing the nba_api, scraping advanced player metrics and historical financial records from reputable sources like Basketball-Reference, and getting team standings from official NBA archives.

* **Integration:** Utilizing Python to resolve entity discrepancies for data cleaning and consistency purposes and performing multi-key joins across player, season, and team identifiers using SQL.

* **Analysis:** Correlate salary levels with performance tiers, identifying outliers who represent high-value player contracts and answering our research questions.

* **Validation:** Documenting our workflow through a reproducible GitHub repository, including data cleaning and integration steps for transparency and automated scripts for data tracking to ensure our project is repeatable and a clear record of how the data was handled.

## Team

### Lead Strategist (Colin Cosillo)

Colin will be responsible for the overall project management with the following key responsibilities:

* **Project Planning & Documentation:** Authoring the project overview, establishing the timeline, and identifying potential constraints or knowledge gaps.

* **Regulatory & Ethical Compliance:** Researching the terms of service for our data sources and ensuring our data handling meets course ethical standards.

* **Quality Assurance:** Reviewing the final comparative model to ensure it addresses our core research questions and remains aligned with the project's goals.

* **Milestone Management:** Managing the GitHub repository's administrative tasks, including tagging releases and submitting documentation to Canvas.

### Lead Architect (Daniel Kang)

Daniel will be responsible for the technical infrastructure and ensuring project reproducibility. Key responsibilities include:

* **Data Acquisition & Pipeline:** Writing the Python scripts to interface with the nba_api and developing the web scraping logic for financial data.

* **System Integration:** Designing the schema for our master dataset and implementing the logic for "Entity Resolution" to link players across different naming conventions.

* **Workflow Automation:** Setting up the project’s directory structure and creating the "Run All" script to ensure the entire analysis can be reproduced with a single command.

* **Storage Strategy:** Managing the data/raw and data/processed environments and ensuring that all data artifacts are stored with proper versioning and provenance.

### Shared Responsibilities

* **Collaborative Coding:** Both members will participate in code reviews and contribute to the Python scripts, with individual contributions clearly documented through Git commit history.

* **Data Cleaning:** We will split the cleaning tasks, with each of us cleaning the same number of datasets. One will focus on performance metrics and the other on financial/salary normalization.

* **Final Reporting:** Collaborating on the interpretation of results and the creation of data visualizations for the final project submission.

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
https://www.nba.com/stats/players/traditional 
https://www.basketball-reference.com/leagues/NBA_2026_advanced.html (advanced metrics data)
https://www.hoopshype.com/salaries/players/ (salary data)
https://www.nba.com/standings (team performance)

Key Attributes: Player_Name (String), Season (Integer), Salary (Numeric), Team_Affiliation (String).

Source: Financial tracking databases (e.g., HoopsHype or Spotrac).

**NBA Team Standings (Success Metrics)**

Description: Data regarding team-level success to determine if team winning percentage correlates with individual overpayment.

Key Attributes: Team_Name (String), Win_Loss_Percentage (Float), Playoff_Appearance (Boolean).

Source: Official NBA historical standings.

## Timeline

## Project Timeline

The following timeline outlines our roadmap from data acquisition to the final project delivery. We have distributed tasks to ensure that data integration is completed early, allowing ample time for analysis and documentation.

| Phase | Task | Description | Deadline | Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **Milestone 2** | **Project Plan Submission** | Finalize ProjectPlan.md, create GitHub tag/release, and submit URL to Canvas. | March 8, 2026 | Lead Strategist |
| **Acquisition** | **Raw Data Harvesting** | Run `nba_api` scripts and Basketball-Reference exports to populate `data/raw/`. | March 15, 2026 | Lead Architect |
| **Acquisition** | **Salary Web Scraping** | Execute BeautifulSoup/Requests script to scrape HoopsHype financial data. | March 18, 2026 | Lead Architect |
| **Integration** | **SQL Database Setup** | Design the schema and initialize a SQLite database to house the normalized raw tables. | March 22, 2026 | Lead Architect |
| **Integration** | **Entity Resolution & Load** | Use SQL/Python to clean names and load data into the database, ensuring referential integrity. | March 25, 2026 | Lead Architect |
| **Integration** | **SQL Table Merging** | Write SQL `JOIN` queries to create the master analytical view in `data/processed/`. | April 1, 2026 | Both |
| **Milestone 3** | **Interim Status Report** | Complete the ~1500-word report documenting progress and SQL integration logic. | April 8, 2026 | Lead Strategist |
| **Analysis** | **Value Modeling** | Calculate efficiency-to-salary ratios and identify statistical outliers (undervalued players). | April 15, 2026 | Both |
| **Analysis** | **Visualization** | Create charts in Python (Matplotlib/Seaborn) using data queried directly from the SQL database. | April 22, 2026 | Lead Strategist |
| **Finalization** | **Workflow Automation** | Finalize the `main.py` or Snakemake file to automate the SQL loading and joining process. | April 29, 2026 | Lead Architect |
| **Finalization** | **Final Report & Release** | Complete final documentation, perform a reproducibility check, and create the final GitHub release. | May 6, 2026 | Both |

## Constraints

We anticipate certain technical and legal constraints that may impact our workflow:
* **API Rate Limiting:** The `nba_api` often throttles requests. We must implement time delays in our scripts to ensure the acquisition process is stable and reproducible.
* **Entity Resolution:** NBA player names often include suffixes (Jr., III) or special characters (e.g., Luka Dončić). Our integration logic must account for these to avoid "null" values during our SQL joins.
* **Data Privacy & Terms of Use:** While the data is public, we must comply with the robots.txt and Terms of Service for Basketball-Reference and HoopsHype to ensure ethical scraping practices.
* **Data Sparsity:** Salary data for "two-way" players or 10-day contract athletes may be incomplete, requiring us to set a "Minimum Minutes Played" threshold for our analysis.

## Gaps

To successfully execute this plan, our team identifies the following gaps where further learning is required:
* **Advanced SQL Joins:** While we are familiar with basic SQL, we need to master complex joins and views within SQLite to ensure our integrated master table is optimized for analysis.
* **Workflow Automation** We need to research how to use Snakemake or similar tools to link our Python acquisition scripts with our SQL integration scripts into a single, automated pipeline.
* **Provenance Standards:** We need to further investigate how to properly document the "lineage" of our data within the GitHub repository to meet the course's transparency requirements.

## Data Lifecycle and Storage Strategy

As the lead for data architecture, I will oversee the following lifecycle:

Ingestion: Data will be collected via Python-based web scraping and API calls. Raw files will be initially stored in a data/raw/ directory in .csv format to preserve the original provenance.

Processing & Cleaning: * Schema Standardization: Ensuring all column names follow snake_case and data types (e.g., converting salary strings like "$40M" to float values) are consistent.

Entity Resolution: Standardizing player names (e.g., "Luka Doncic" vs "Luka Dončić") to ensure seamless joining across different sources.

Storage & Organization: * Processed data will be stored in data/processed/ as a master integrated file.

For the GitHub repository, I will implement a clear directory structure to separate the document schema from the actual analysis scripts, ensuring the project remains scalable and organized.
