import sqlite3
import pandas as pd
import os

print("=" * 60)
print("STEP 1: Load Raw CSV to SQLite")
print("=" * 60)

# Paths (using ../ to go from scripts/ to project root)
csv_path = '../data/raw/nba_2025_26_raw.csv'
db_path = '../database/nba_2025_26.db'

# Create database folder if it doesn't exist
os.makedirs('../database', exist_ok=True)

# Check if CSV exists
if not os.path.exists(csv_path):
    print(f"❌ ERROR: CSV not found at {csv_path}")
    exit(1)

# Load CSV
df = pd.read_csv(csv_path)
print(f"✅ Loaded {len(df)} rows from CSV")

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Save to raw_players table
df.to_sql('raw_players', conn, if_exists='replace', index=False)
print(f"✅ Saved to 'raw_players' table at {db_path}")

conn.close()
print("\n✅ STEP 1 COMPLETE!")