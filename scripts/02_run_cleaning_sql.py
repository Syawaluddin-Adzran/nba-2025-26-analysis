import sqlite3
import pandas as pd
import os

print("=" * 60)
print("STEP 2: Clean and Aggregate Data (SQL-Only)")
print("=" * 60)

db_path = '../database/nba_2025_26.db'

# Connect to database
conn = sqlite3.connect(db_path)

# ============================================
# STEP 1: Drop old tables if they exist
# ============================================
conn.execute("DROP TABLE IF EXISTS cleaned_players")
conn.execute("DROP TABLE IF EXISTS player_aggregated")

print("✅ Cleaned old tables")

# ============================================
# STEP 2: Aggregate players in SQL
# ============================================
print("\n🔄 Aggregating players in SQL...")

conn.execute("""
CREATE TABLE player_aggregated AS
SELECT 
    Player,
    MAX(Age) AS Age,
    MAX(Pos) AS Pos,
    SUM(MP) AS MP,
    SUM(PTS) AS PTS,
    SUM(FG) AS FG,
    SUM(FGA) AS FGA,
    SUM(CAST("3P" AS INTEGER)) AS "3P",
    SUM("3PA") AS "3PA",
    SUM(FT) AS FT,
    SUM(FTA) AS FTA,
    SUM(TRB) AS TRB,
    SUM(AST) AS AST,
    SUM(STL) AS STL,
    SUM(BLK) AS BLK,
    SUM(TOV) AS TOV,
    -- Determine team: take real team with most minutes (exclude TM codes)
    (
        SELECT Team FROM raw_players r2 
        WHERE r2.Player = r1.Player 
          AND r2.Team NOT LIKE '%TM'
        ORDER BY r2.MP DESC LIMIT 1
    ) AS Team
FROM raw_players r1
GROUP BY Player
""")

print("✅ Player aggregation complete")

# ============================================
# STEP 3: Calculate percentages and PPM in SQL
# ============================================
print("\n📐 Calculating percentages and PPM...")

conn.execute("""
CREATE TABLE cleaned_players AS
SELECT 
    Player,
    Age,
    Team,
    Pos,
    MP,
    PTS,
    ROUND(CAST(PTS AS FLOAT) / FGA, 3) AS FG_Pct,
    ROUND(CAST("3P" AS FLOAT) / "3PA", 3) AS ThreeP_Pct,
    ROUND(CAST(FT AS FLOAT) / FTA, 3) AS FT_Pct,
    TRB,
    AST,
    STL,
    BLK,
    TOV,
    ROUND(CAST(PTS AS FLOAT) / MP, 3) AS PPM
FROM player_aggregated
WHERE MP > 100
  AND Team IS NOT NULL
  AND Team NOT LIKE '%TM'
""")

print("✅ Percentages and PPM calculated")

# ============================================
# STEP 4: Verify row count
# ============================================
result = conn.execute("SELECT COUNT(*) FROM cleaned_players").fetchone()
print(f"\n📊 Final cleaned_players: {result[0]} rows")

# ============================================
# STEP 5: Export to CSV
# ============================================
print("\n💾 Exporting to CSV...")

df_clean = pd.read_sql_query("SELECT * FROM cleaned_players", conn)
os.makedirs('../data/cleaned', exist_ok=True)
df_clean.to_csv('../data/cleaned/nba_2025_26_cleaned.csv', index=False)
print(f"✅ Saved CSV to ../data/cleaned/nba_2025_26_cleaned.csv")

conn.close()
print("\n✅ STEP 2 COMPLETE!")