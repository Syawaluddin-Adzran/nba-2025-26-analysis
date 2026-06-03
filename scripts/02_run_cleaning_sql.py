import sqlite3
import pandas as pd
import os

print("=" * 60)
print("STEP 2: Clean and Aggregate Data")
print("=" * 60)

db_path = '../database/nba_2025_26.db'

# Connect to database
conn = sqlite3.connect(db_path)

# Load raw data
df_raw = pd.read_sql_query("SELECT * FROM raw_players", conn)
print(f"✅ Loaded {len(df_raw)} rows from raw_players")

# ============================================
# Aggregate by player (combine individual team rows)
# ============================================
print("\n🔄 Aggregating by player...")

df_clean = df_raw.groupby('Player').agg({
    'Age': 'max',
    'Pos': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'MP': 'sum',
    'PTS': 'sum',
    'FG': 'sum',
    'FGA': 'sum',
    '3P': 'sum',
    '3PA': 'sum',
    'FT': 'sum',
    'FTA': 'sum',
    'TRB': 'sum',
    'AST': 'sum',
    'STL': 'sum',
    'BLK': 'sum',
    'TOV': 'sum'
}).reset_index()

# Determine Team (take the one with most minutes)
def get_team(group):
    if any('TM' in str(t) for t in group['Team']):
        return group[group['Team'].str.contains('TM', na=False)].iloc[0]['Team']
    else:
        return group.loc[group['MP'].idxmax(), 'Team']

team_map = df_raw.groupby('Player').apply(get_team).reset_index()
team_map.columns = ['Player', 'Team']
df_clean = df_clean.merge(team_map, on='Player', how='left')

# Calculate percentages
df_clean['FG_Pct'] = round(df_clean['PTS'] / df_clean['FGA'], 3)
df_clean['ThreeP_Pct'] = round(df_clean['3P'] / df_clean['3PA'], 3)
df_clean['FT_Pct'] = round(df_clean['FT'] / df_clean['FTA'], 3)
df_clean['PPM'] = round(df_clean['PTS'] / df_clean['MP'], 3)

# Filter out low minutes
df_clean = df_clean[df_clean['MP'] > 100]

# ============================================
# CRITICAL FIX: Exclude fake teams (2TM, 3TM, 4TM)
# ============================================
print("\n🚫 Excluding fake teams (2TM, 3TM, 4TM)...")
before = len(df_clean)
df_clean = df_clean[~df_clean['Team'].str.contains('TM', na=False)]
after = len(df_clean)
print(f"   Removed {before - after} rows with fake team codes")

# ============================================
# Verify James Harden is gone (he's now assigned to a real team)
# ============================================
harden = df_clean[df_clean['Player'] == 'James Harden']
if len(harden) > 0:
    print(f"\n📋 James Harden now has real team: {harden['Team'].iloc[0]}")
else:
    print("\n⚠️ James Harden not found – check aggregation")

print(f"\n✅ Final cleaned data: {len(df_clean)} rows (one per player, real teams only)")

# ============================================
# Save to database and CSV
# ============================================
print("\n💾 Saving to database...")
df_clean.to_sql('cleaned_players', conn, if_exists='replace', index=False)
print(f"✅ Saved to 'cleaned_players' table")

os.makedirs('../data/cleaned', exist_ok=True)
df_clean.to_csv('../data/cleaned/nba_2025_26_cleaned.csv', index=False)
print(f"✅ Saved CSV to ../data/cleaned/nba_2025_26_cleaned.csv")

conn.close()
print("\n✅ STEP 2 COMPLETE!")