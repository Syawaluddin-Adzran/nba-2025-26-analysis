import sqlite3
import pandas as pd
import os

# Paths
raw_csv_path = '../data/raw/nba_2025_26_raw.csv'
db_path = '../database/nba_2025_26.db'
cleaned_csv_path = '../data/cleaned/nba_2025_26_cleaned.csv'

# Ensure directories exist
os.makedirs(os.path.dirname(db_path), exist_ok=True)
os.makedirs(os.path.dirname(cleaned_csv_path), exist_ok=True)

# -------------------------------
# 1. Load raw CSV
# -------------------------------
print(f"📂 Loading CSV from: {raw_csv_path}")
df_raw = pd.read_csv(raw_csv_path)

# Drop the final "League Average" row (where Player is missing)
df_raw = df_raw[df_raw['Player'].notna()].copy()

print(f"✅ Loaded {len(df_raw)} rows (after removing footer)")

# -------------------------------
# 2. Clean column names (strip spaces, fix special names)
# -------------------------------
df_raw.columns = [col.strip() for col in df_raw.columns]

# Ensure numeric columns are properly typed
numeric_cols = ['Age', 'MP', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
for col in numeric_cols:
    if col in df_raw.columns:
        df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

# -------------------------------
# 3. Load into SQLite
# -------------------------------
conn = sqlite3.connect(db_path)
df_raw.to_sql('raw_players', conn, if_exists='replace', index=False)
print(f"✅ Loaded raw data into raw_players table")

# Drop old cleaned table if exists
conn.execute("DROP TABLE IF EXISTS cleaned_players")

# -------------------------------
# 4. Create cleaned_players table using SQL with quoted identifiers
# -------------------------------
print("\n🔄 Creating cleaned_players table...")

conn.execute("""
CREATE TABLE cleaned_players AS
SELECT 
    Player,
    Age,
    CASE 
        WHEN Team IS NULL OR Team = '' THEN 'Unknown'
        ELSE Team
    END AS Team,
    CASE 
        WHEN Pos IS NULL OR Pos = '' THEN 'Unknown'
        WHEN Pos LIKE '%-%' THEN SUBSTR(Pos, 1, INSTR(Pos, '-') - 1)
        ELSE Pos
    END AS Pos,
    MP,
    PTS,
    ROUND(CAST(FG AS FLOAT) / NULLIF(FGA, 0), 3) AS FG_Pct,
    ROUND(CAST("3P" AS FLOAT) / NULLIF("3PA", 0), 3) AS ThreeP_Pct,
    ROUND(CAST(FT AS FLOAT) / NULLIF(FTA, 0), 3) AS FT_Pct,
    TRB,
    AST,
    STL,
    BLK,
    TOV,
    PF,
    ROUND(CAST(PTS AS FLOAT) / NULLIF(MP, 0), 3) AS PPM
FROM raw_players
WHERE MP > 100
  AND (Team NOT LIKE '%TM' OR Team IS NULL)
""")

# -------------------------------
# 5. Verify results
# -------------------------------
count = conn.execute("SELECT COUNT(*) FROM cleaned_players").fetchone()[0]
print(f"✅ Cleaned table created with {count} rows")

unknown_count = conn.execute("SELECT COUNT(*) FROM cleaned_players WHERE Team = 'Unknown'").fetchone()[0]
if unknown_count > 0:
    print(f"   (Note: {unknown_count} players have 'Unknown' team)")

# -------------------------------
# 6. Export cleaned data to CSV
# -------------------------------
df_clean = pd.read_sql_query("SELECT * FROM cleaned_players", conn)
df_clean.to_csv(cleaned_csv_path, index=False)
print(f"💾 Cleaned data saved to: {cleaned_csv_path}")

conn.close()
print("\n✅ ALL DONE! Database and cleaned CSV are ready.")