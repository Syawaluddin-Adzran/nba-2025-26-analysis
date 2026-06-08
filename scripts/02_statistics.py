import sqlite3
import pandas as pd

print("=" * 60)
print("STEP 3: Analysis (Player + Team)")
print("=" * 60)

db_path = '../database/nba_2025_26.db'

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM cleaned_players", conn)
conn.close()

print(f"📊 Loaded {len(df)} players (minimum 100 MP, no aggregate teams)\n")

# ============================================
# 1. Correlation (full dataset: MP > 100)
# ============================================
correlation_all = df['MP'].corr(df['PTS'])
print(f"📈 Correlation (Minutes vs Points) - ALL players (MP > 100): {correlation_all:.3f}")
print(f"   R-squared: {correlation_all**2:.3f}")

# ============================================
# 2. Correlation (players with >500 minutes)
# ============================================
df_500 = df[df['MP'] > 500]
correlation_500 = df_500['MP'].corr(df_500['PTS'])
print(f"\n📈 Correlation (Minutes vs Points) - players with MP > 500: {correlation_500:.3f}")

# ============================================
# 3. Correlation (players with >1000 minutes)
# ============================================
df_1000 = df[df['MP'] > 1000]
correlation_1000 = df_1000['MP'].corr(df_1000['PTS'])
print(f"\n📈 Correlation (Minutes vs Points) - players with MP > 1000: {correlation_1000:.3f}")

# ============================================
# 4. Top 10 by PPM (minimum 500 minutes)
# ============================================
top_ppm = df_500.nlargest(10, 'PPM')[['Player', 'Team', 'Pos', 'PPM', 'PTS', 'MP']]
print("\n🏆 Top 10 by Points Per Minute (PPM) - minimum 500 MP:")
print(top_ppm.to_string(index=False))

# ============================================
# 5. Position averages
# ============================================
position_avg = df.groupby('Pos')[['PTS', 'MP', 'PPM']].mean().round(2)
position_avg.columns = ['Avg Points', 'Avg Minutes', 'Avg PPM']
print("\n📊 Average by Position:")
print(position_avg)

# ============================================
# 6. TEAM ANALYSIS (only real teams – already filtered in cleaned_players)
# ============================================
print("\n" + "=" * 60)
print("TEAM ANALYSIS (Real Teams Only)")
print("=" * 60)

# 6.1 Team summary
team_summary = df.groupby('Team').agg({
    'Player': 'count',
    'PTS': 'sum',
    'MP': 'sum',
    'PPM': 'mean'
}).round(2).rename(columns={'Player': 'Num_Players'})
team_summary.columns = ['Players', 'Total_Points', 'Total_Minutes', 'Avg_PPM']
team_summary = team_summary.sort_values('Total_Points', ascending=False)

print("\n🏢 Team Summary (sorted by total points):")
print(team_summary.head(10).to_string())

# 6.2 Most efficient team
top_team_ppm = team_summary.nlargest(5, 'Avg_PPM')[['Players', 'Total_Points', 'Avg_PPM']]
print("\n⚡ Top 5 Most Efficient Teams (by Avg PPM):")
print(top_team_ppm.to_string())

# 6.3 Team with most players in top 100 scorers
top100_players = df.nlargest(100, 'PTS')
team_top100_count = top100_players['Team'].value_counts().head(5)
print("\n🏆 Teams with most players in Top 100 Scorers:")
for team, count in team_top100_count.items():
    print(f"   {team}: {count} player(s)")

# 6.4 Best player per team
best_per_team = df.loc[df.groupby('Team')['PPM'].idxmax()][['Team', 'Player', 'Pos', 'PPM', 'PTS', 'MP']]
best_per_team = best_per_team.sort_values('Team')
print("\n🌟 Best Player per Team (by PPM):")
print(best_per_team.to_string(index=False))

# ============================================
# 7. Summary statistics
# ============================================
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(f"   Total players (MP > 100): {len(df)}")
print(f"   Total teams: {df['Team'].nunique()}")
print(f"   Total points scored: {df['PTS'].sum():,.0f}")
print(f"   Total minutes played: {df['MP'].sum():,.0f}")
print(f"   Average points per player: {df['PTS'].mean():.1f}")
print(f"   Average minutes per player: {df['MP'].mean():.1f}")
print(f"   League average PPM: {df['PPM'].mean():.3f}")
print(f"   League average FG%: {df['FG_Pct'].mean():.3f}")
print(f"   League average 3P%: {df['ThreeP_Pct'].mean():.3f}")
print(f"   League average FT%: {df['FT_Pct'].mean():.3f}")

print("\n✅ STEP 3 COMPLETE!")