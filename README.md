# 🏀 NBA 2025-26 Season Analysis

**End-to-End Data Analytics Project using SQL, Python, SQLite, Visualization, and Streamlit**

## 📌 Project Overview

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

## ❓ Business Question

A common assumption in basketball is:

> "Players score more simply because they play more minutes."

This project investigates whether playing time alone explains scoring output and introduces a custom metric to evaluate scoring efficiency independently of minutes played.

---

## 📈 Custom Metric: Points Per Minute (PPM)

To measure scoring efficiency, I created:

**PPM = Total Points ÷ Total Minutes Played**

This metric helps identify players who score efficiently regardless of total playing time.

### Why PPM?

* Removes the advantage of simply playing more minutes
* Highlights efficient scorers
* Enables fair comparison across players
* Complements traditional metrics such as total points and points per game

---

## 🔄 Data Pipeline

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

## 🧹 Data Cleaning

- Removed the "League Average" footer row
- Excluded aggregate team rows (`2TM`, `3TM`) – these combine stats from multiple teams
- Kept **one row per player per actual team** (traded players appear once for each team)
- Filtered to players with **minimum 100 minutes played** (removes garbage‑time players)

**Result:** 734 raw records → 549 cleaned records (minimum 100 MP, no aggregate teams)

---

## 🔑 Key Findings

### Minutes Strongly Predict Points

| Group         | Correlation |
|---------------|-------------|
| All Players (MP > 100) | 0.908       |
| >500 Minutes  | 0.862       |
| >1000 Minutes | 0.783       |

The relationship weakens among high‑minute players (from **0.908** down to **0.783**), suggesting that efficiency becomes increasingly important at higher levels of competition.

### Most Efficient Scorers (PPM, minimum 500 MP)

| Player                  | Team | Pos | PPM  |
|------------------------|------|-----|------|
| Giannis Antetokounmpo  | MIL  | PF  | 0.956 |
| Shai Gilgeous-Alexander| OKC  | PG  | 0.937 |
| Luka Dončić            | LAL  | PG  | 0.936 |
| Kawhi Leonard          | LAC  | SF  | 0.870 |
| Stephen Curry          | GSW  | PG  | 0.859 |
| Victor Wembanyama      | SAS  | C   | 0.857 |
| Joel Embiid            | PHI  | C   | 0.850 |
| Jaylen Brown           | BOS  | SF  | 0.834 |
| Donovan Mitchell       | CLE  | SG  | 0.833 |
| Anthony Edwards        | MIN  | SG  | 0.822 |

### Position Analysis

Point Guards recorded the highest average PPM (0.47), indicating superior scoring efficiency relative to playing time.

### Team Analysis

* **Most efficient team** (highest average PPM): Miami Heat (0.49)
* **Highest total points scored**: Denver Nuggets (9,910 points)
* **Deepest scoring roster** (most players in Top 100 scorers): San Antonio Spurs (6 players)

---

## 📉 Visualizations

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

## 📊 Interactive Dashboard

The Streamlit dashboard allows users to:

* Filter by team
* Filter by position
* Filter by minutes played
* Explore scoring leaders
* Compare player efficiency
* Analyze team performance
* Visualize scoring distributions

---

## 🧰 Tech Stack

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

## 📁 Repository Structure

```text
nba-2025-26-analysis/
│
├── data/
│   ├── raw/
│   │   └── nba_2025_26_raw.csv
│   └── cleaned/
│       └── nba_2025_26_cleaned.csv
│
├── database/
│   └── nba_2025_26.db
│
├── scripts/
│   ├── 01_run_cleaning_sql.py
│   ├── 02_statistics.py
│   ├── 03_visualizations.py
│   └── nba_dashboard.py
│
├── outputs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Running the Project

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
python scripts/01_run_cleaning_sql.py
python scripts/02_statistics.py
python scripts/03_visualizations.py
```

### Launch Dashboard

```bash
streamlit run scripts/nba_dashboard.py
```

---

## 🧠 Skills Demonstrated

- Data Cleaning  
- SQL Querying  
- Database Design  
- Exploratory Data Analysis (EDA)  
- Statistical Analysis  
- Feature Engineering  
- Data Visualization  
- Dashboard Development  
- Cloud Deployment  
- Git Version Control  

---

## 📚 Data Source

Basketball Reference  
Source: https://www.basketball-reference.com/

Data was downloaded manually through the official export feature for educational and non-commercial purposes.

---

## 🔮 Future Improvements

- Add defensive metrics (steals, blocks, defensive rating)  
- Integrate salary data for value analysis  
- Perform season-over-season comparisons  
- Build predictive player-performance models  
- Integrate NBA API for automated updates  

---

## 👤 Author

Muhammad Syawaluddin Bin Adzran

- GitHub: https://github.com/Syawaluddin-Adzran  
- LinkedIn: https://www.linkedin.com/in/muhammad-syawaluddin-bin-adzran  

---

## 🏁 Final Note

Built as a portfolio project to demonstrate end-to-end data analytics skills using real-world sports data.