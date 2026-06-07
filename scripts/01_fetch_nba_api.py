import pandas as pd
import os
from nba_api.stats.endpoints import commonallplayers, playercareerstats
import time

SEASON = "2025-26"

# Create output directory if it doesn't exist
os.makedirs('data/raw', exist_ok=True)

print("Fetching all NBA players...")
players = commonallplayers.CommonAllPlayers(league_id="00", season=SEASON, is_only_current_season=1)
players_df = players.get_data_frames()[0]
print(f"Fetched {len(players_df)} players.")

all_stats = []

for idx, row in players_df.iterrows():
    player_id = row['PERSON_ID']
    name = row['DISPLAY_LAST_COMMA_FIRST']
    print(f"Fetching stats for {name} (ID: {player_id})...")

    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_df = career.get_data_frames()[0]
        season_row = career_df[career_df['SEASON_ID'] == SEASON]
        if not season_row.empty:
            all_stats.append(season_row.iloc[0])
    except Exception as e:
        print(f"Error for {name}: {e}")

    time.sleep(0.2)

if not all_stats:
    print("No season stats found. Check SEASON format (e.g., '2025-26').")
else:
    final_df = pd.DataFrame(all_stats)

    # Merge with basic player info (only ID and name, skip position/team to avoid missing columns)
    final_df = final_df.merge(
        players_df[['PERSON_ID', 'DISPLAY_LAST_COMMA_FIRST']],
        left_on='PLAYER_ID', right_on='PERSON_ID',
        how='left'
    )
    final_df['Player'] = final_df['DISPLAY_LAST_COMMA_FIRST']

    # Rename columns to match your pipeline (only those that exist)
    rename_map = {
        'GP': 'G',
        'MIN': 'MP',
        'PTS': 'PTS',
        'FG_PCT': 'FG%',
        'FG3_PCT': '3P%',
        'FT_PCT': 'FT%',
        'REB': 'TRB',
        'AST': 'AST',
        'STL': 'STL',
        'BLK': 'BLK',
        'TOV': 'TOV',
        'PF': 'PF'
    }
    final_df = final_df.rename(columns={k: v for k, v in rename_map.items() if k in final_df.columns})

    # Add placeholder columns for Team and Pos if missing (to match your pipeline)
    if 'Team' not in final_df.columns:
        final_df['Team'] = ''
    if 'Pos' not in final_df.columns:
        final_df['Pos'] = ''

    # Select columns in order
    column_order = ['Player', 'Team', 'Pos', 'G', 'MP', 'PTS', 'FG%', '3P%', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 'TOV',
                    'PF']
    final_df = final_df[[col for col in column_order if col in final_df.columns]]

    output_path = 'data/raw/nba_2025_26_raw.csv'
    final_df.to_csv(output_path, index=False)
    print(f"Saved {len(final_df)} player records to {output_path}")