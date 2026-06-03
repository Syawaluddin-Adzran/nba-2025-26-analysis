# 🏀 NBA 2025-26 Season Analysis

**End-to-End Data Analytics Project using SQL, Python, SQLite, Visualization, and Streamlit**

## Project Overview

This project explores the relationship between playing time and scoring production in the NBA. Using player statistics from the 2025-26 NBA season, I built a complete analytics pipeline that transforms raw data into actionable insights through statistical analysis, visualizations, and an interactive dashboard.

The project demonstrates practical data analyst skills including:

* SQL data cleaning and transformation
* Database management with SQLite
* Data analysis with Python and pandas
* Statistical analysis and correlation testing
* Data visualization with matplotlib and seaborn
* Dashboard development using Streamlit
* Deployment using Streamlit Cloud

---

## Business Question

A common assumption in basketball is:

> "Players score more simply because they play more minutes."

This project investigates whether playing time alone explains scoring output and introduces a custom metric to evaluate scoring efficiency independently of minutes played.

---

## Custom Metric: Points Per Minute (PPM)

To measure scoring efficiency, I created:

PPM = Total Points ÷ Total Minutes Played

This metric helps identify players who score efficiently regardless of total playing time.

### Why PPM?

* Removes the advantage of simply playing more minutes
* Highlights efficient scorers
* Enables fair comparison across players
* Complements traditional metrics such as total points and points per game

---

## Data Pipeline

Raw CSV (Basketball Reference)

↓

SQLite Database

↓

SQL Cleaning & Transformation

↓

Python Statistical Analysis

↓

Visualizations

↓

Interactive Streamlit Dashboard

↓

Cloud Deployment

---

## Data Cleaning

The dataset contained players who appeared for multiple teams during the season.

Example:

| Player       | Team |
|--------------|------|
| James Harden | LAC  |
| James Harden | CLE  |
| James Harden | 2TM  |

To avoid double-counting, only the aggregated `2TM` record was retained.

Result:

* Raw records: 734
* Final records: 503 unique players

---

## Key Findings

### Minutes Strongly Predict Points

| Group         | Correlation |
|---------------|-------------|
| All Players   | 0.901       |
| >500 Minutes  | 0.855       |
| >1000 Minutes | 0.792       |

The relationship weakens among high-minute players, suggesting that efficiency becomes increasingly important at higher levels of competition.

### Most Efficient Scorers

Top performers by PPM include:

* Giannis Antetokounmpo
* Shai Gilgeous-Alexander
* Luka Dončić
* Kawhi Leonard
* Stephen Curry

### Position Analysis

Point Guards recorded the highest average PPM, indicating superior scoring efficiency relative to playing time.

### Team Analysis

Key team-level insights include:

* Miami Heat recorded the highest team efficiency.
* Denver Nuggets generated the highest total points.
* San Antonio Spurs had the deepest scoring roster based on top-100 scorers.

---

## Visualizations

The project generates multiple analytical visualizations, including:

* Minutes vs Points scatter plots
* Correlation comparisons
* Team scoring rankings
* Team efficiency rankings
* Position efficiency boxplots
* PPM distribution analysis
* Top scorer leaderboards

All generated charts are stored in the `/outputs` directory.

---

## Interactive Dashboard

The Streamlit dashboard allows users to:

* Filter by team
* Filter by position
* Filter by minutes played
* Explore scoring leaders
* Compare player efficiency
* Analyze team performance
* Visualize scoring distributions

---

## Tech Stack

| Category        | Tools                       |
|-----------------|-----------------------------|
| Database        | SQLite                      |
| Query Language  | SQL                         |
| Analysis        | Python, pandas, NumPy       |
| Statistics      | SciPy                       |
| Visualization   | matplotlib, seaborn, Plotly |
| Dashboard       | Streamlit                   |
| Deployment      | Streamlit Cloud             |
| Version Control | Git, GitHub                 |

---

## Repository Structure

```text
nba-2025-26-analysis/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── scripts/
│   ├── 01_load_raw_to_sql.py
│   ├── 02_clean_and_aggregate.py
│   ├── 03_analysis.py
│   ├── 04_visualizations.py
│   └── nba_dashboard.py
│
├── outputs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Project

### Clone Repository

```bash
git clone https://github.com/Syawaluddin-Adzran/nba-2025-26-analysis.git
cd nba-2025-26-analysis
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Execute Pipeline

```bash
python scripts/01_load_raw_to_sql.py
python scripts/02_clean_and_aggregate.py
python scripts/03_analysis.py
python scripts/04_visualizations.py
```

### Launch Dashboard

```bash
streamlit run scripts/nba_dashboard.py
```

---

## Skills Demonstrated

* Data Cleaning
* SQL Querying
* Database Design
* Exploratory Data Analysis (EDA)
* Statistical Analysis
* Feature Engineering
* Data Visualization
* Dashboard Development
* Cloud Deployment
* Git Version Control

---

## Data Source

Basketball Reference

Source: https://www.basketball-reference.com/

Data was downloaded manually through the official export feature for educational and non-commercial purposes.

---

## Future Improvements

* Add defensive metrics
* Integrate salary data
* Perform season-over-season comparisons
* Build predictive player-performance models
* Integrate NBA API for automated updates

---

## Author

**Muhammad Syawaluddin Bin Adzran**

* GitHub: https://github.com/Syawaluddin-Adzran
* LinkedIn: Add your LinkedIn URL

---

Built as a portfolio project to demonstrate end-to-end data analytics skills using real-world sports data.
