import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from scipy import stats

print("=" * 60)
print("STEP 4: Visualizations (Consistent Colors)")
print("=" * 60)

db_path = '../database/nba_2025_26.db'

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM cleaned_players", conn)
conn.close()

print(f"📊 Loaded {len(df)} players\n")

# Filter out fake teams for team charts
real_teams = df[~df['Team'].str.contains('TM', na=False)]
print(f"📊 Real teams only (excludes 2TM/3TM/4TM): {len(real_teams)} players\n")

# Create outputs folder
os.makedirs('../outputs', exist_ok=True)

# Set style
sns.set_style("whitegrid")

# Position colors
position_colors = {'PG': 'blue', 'SG': 'green', 'SF': 'orange', 'PF': 'purple', 'C': 'red'}

# ============================================
# CREATE CONSISTENT TEAM COLOR MAP (SAME FOR ALL CHARTS)
# ============================================
all_teams = sorted(real_teams['Team'].unique())
num_teams = len(all_teams)
team_color_map = {}
team_colors_list = plt.cm.tab20(np.linspace(0, 1, num_teams))
for i, team in enumerate(all_teams):
    team_color_map[team] = team_colors_list[i]

# ============================================
# CHART 1: Correlation Comparison
# ============================================
print("📊 Creating Chart 1: Correlation Comparison...")

corr_all = df['MP'].corr(df['PTS'])
corr_500 = df[df['MP'] > 500]['MP'].corr(df[df['MP'] > 500]['PTS'])
corr_1000 = df[df['MP'] > 1000]['MP'].corr(df[df['MP'] > 1000]['PTS'])

corr_data = pd.DataFrame({
    'Group': ['All Players', '>500 Minutes', '>1000 Minutes'],
    'Correlation': [corr_all, corr_500, corr_1000]
})

plt.figure(figsize=(8, 5))
bars = plt.bar(corr_data['Group'], corr_data['Correlation'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Moderate correlation line')
plt.ylabel('Correlation (r)')
plt.title('Minutes vs Points Correlation by Player Group')
plt.ylim(0, 1)
for bar, val in zip(bars, corr_data['Correlation']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val:.3f}', ha='center', fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig('../outputs/correlation_comparison.png', dpi=150)
plt.close()
print("   ✅ Saved: correlation_comparison.png")

# ============================================
# CHART 2: Top 10 Teams by Total Points
# ============================================
print("📊 Creating Chart 2: Top Teams by Total Points...")

team_points = real_teams.groupby('Team')['PTS'].sum().sort_values(ascending=False).head(10)
team_points_colors = [team_color_map[team] for team in team_points.index]

plt.figure(figsize=(10, 6))
plt.barh(team_points.index, team_points.values, color=team_points_colors)
plt.xlabel('Total Points')
plt.title('Top 10 Teams by Total Points Scored')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('../outputs/top_teams_by_points.png', dpi=150)
plt.close()
print("   ✅ Saved: top_teams_by_points.png")

# ============================================
# CHART 3: Top 10 Team Efficiency
# ============================================
print("📊 Creating Chart 3: Team Efficiency...")

team_eff = real_teams.groupby('Team')['PPM'].mean().sort_values(ascending=False).head(10)
team_eff_colors = [team_color_map[team] for team in team_eff.index]

plt.figure(figsize=(10, 6))
plt.barh(team_eff.index, team_eff.values, color=team_eff_colors)
plt.xlabel('Average Points Per Minute (PPM)')
plt.title('Top 10 Most Efficient Teams')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('../outputs/top_teams_efficiency.png', dpi=150)
plt.close()
print("   ✅ Saved: top_teams_efficiency.png")

# ============================================
# CHART 4: Best Player per Team (Scatter)
# ============================================
print("📊 Creating Chart 4: Best Player per Team...")

best_per_team = real_teams.loc[real_teams.groupby('Team')['PPM'].idxmax()]
best_per_team = best_per_team.sort_values('PPM', ascending=False)

plt.figure(figsize=(14, 8))
for idx, row in best_per_team.iterrows():
    color = team_color_map.get(row['Team'], 'gray')
    plt.scatter(row['PTS'], row['PPM'], s=row['PTS']/8, alpha=0.8, color=color, edgecolors='black', linewidth=0.5)

plt.xlabel('Total Points')
plt.ylabel('PPM (Efficiency)')
plt.title('Best Player per Team: Efficiency vs Volume')

for idx, row in best_per_team.iterrows():
    plt.annotate(f"{row['Player']} ({row['Team']})", (row['PTS'], row['PPM']),
                 fontsize=7, alpha=0.8, xytext=(5, 5), textcoords='offset points')

handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=team_color_map[team],
                      markersize=8, label=team) for team in best_per_team['Team']]
plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)

plt.tight_layout()
plt.savefig('../outputs/best_player_per_team.png', dpi=150)
plt.close()
print("   ✅ Saved: best_player_per_team.png")

# ============================================
# CHART 5: Best Player Efficiency Bar Chart
# ============================================
print("📊 Creating Chart 5: Best Player Efficiency per Team...")

best_per_team_sorted = best_per_team.sort_values('PPM', ascending=False).head(15)

plt.figure(figsize=(12, 8))
colors_best = [team_color_map[team] for team in best_per_team_sorted['Team']]
plt.barh(best_per_team_sorted['Player'] + " (" + best_per_team_sorted['Team'] + ")",
         best_per_team_sorted['PPM'], color=colors_best)
plt.xlabel('Points Per Minute (PPM)')
plt.title('Top 15 Best Player Efficiency by Team (Highest PPM)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('../outputs/best_player_efficiency.png', dpi=150)
plt.close()
print("   ✅ Saved: best_player_efficiency.png")

# ============================================
# CHART 6: Top 10 Scorers (NOW USING SAME TEAM COLORS)
# ============================================
print("📊 Creating Chart 6: Top 10 Scorers...")

top_scorers = df.nlargest(10, 'PTS')[['Player', 'Team', 'PTS']]
top_scorers_colors = [team_color_map.get(team, 'gray') for team in top_scorers['Team']]

plt.figure(figsize=(10, 6))
bars = plt.barh(top_scorers['Player'], top_scorers['PTS'], color=top_scorers_colors)
plt.xlabel('Total Points')
plt.title('Top 10 Scorers (Colored by Team)')
plt.gca().invert_yaxis()

# Add team labels next to player names
for i, (idx, row) in enumerate(top_scorers.iterrows()):
    plt.text(row['PTS'] + 20, i, f"({row['Team']})", va='center', fontsize=9, alpha=0.7)

plt.tight_layout()
plt.savefig('../outputs/top10_scorers.png', dpi=150)
plt.close()
print("   ✅ Saved: top10_scorers.png (now uses team colors)")

# ============================================
# CHART 7: Minutes vs Points Scatter by Position
# ============================================
print("📊 Creating Chart 7: Minutes vs Points by Position...")

plt.figure(figsize=(10, 6))
for pos, color in position_colors.items():
    subset = df[df['Pos'] == pos]
    if len(subset) > 0:
        plt.scatter(subset['MP'], subset['PTS'], label=pos, color=color, alpha=0.6, s=50)
plt.xlabel('Minutes Played')
plt.ylabel('Points')
plt.title('Minutes vs Points by Position')
plt.legend()
plt.tight_layout()
plt.savefig('../outputs/scatter_by_position.png', dpi=150)
plt.close()
print("   ✅ Saved: scatter_by_position.png")

# ============================================
# CHART 8: Efficiency by Position Box Plot
# ============================================
print("📊 Creating Chart 8: Efficiency by Position...")

box_palette = [position_colors[pos] for pos in ['PG', 'SG', 'SF', 'PF', 'C']]
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Pos', y='PPM', order=['PG', 'SG', 'SF', 'PF', 'C'], palette=box_palette)
plt.xlabel('Position')
plt.ylabel('Points Per Minute')
plt.title('Efficiency Distribution by Position')
plt.tight_layout()
plt.savefig('../outputs/boxplot_by_position.png', dpi=150)
plt.close()
print("   ✅ Saved: boxplot_by_position.png")

# ============================================
# CHART 9: Teams with Most Players in Top 100
# ============================================
print("📊 Creating Chart 9: Teams in Top 100...")

top100_players = real_teams.nlargest(100, 'PTS')
team_top100_count = top100_players['Team'].value_counts().head(10)
team_top100_colors = [team_color_map.get(team, 'gray') for team in team_top100_count.index]

plt.figure(figsize=(10, 6))
plt.bar(team_top100_count.index, team_top100_count.values, color=team_top100_colors)
plt.xlabel('Team')
plt.ylabel('Number of Players in Top 100')
plt.title('Teams with Most Players in Top 100 Scorers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('../outputs/teams_top100_scorers.png', dpi=150)
plt.close()
print("   ✅ Saved: teams_top100_scorers.png")

# ============================================
# CHART 10: PPM Distribution with KDE (Bell Curve) + Gradient Colors
# ============================================
print("📊 Creating Chart 10: PPM Distribution with KDE...")

from scipy import stats

plt.figure(figsize=(10, 6))

# Create histogram with gradient colors (density-based)
n, bins, patches = plt.hist(df['PPM'], bins=30, density=True, alpha=0.7, edgecolor='black')

# Color bins by density (higher density = darker color)
for i, patch in enumerate(patches):
    # Get the bin's center value
    bin_center = (bins[i] + bins[i+1]) / 2
    # Normalize to [0,1] for colormap
    norm_val = (bin_center - df['PPM'].min()) / (df['PPM'].max() - df['PPM'].min())
    patch.set_facecolor(plt.cm.plasma(norm_val))

# Calculate KDE (bell curve)
kde_x = np.linspace(df['PPM'].min(), df['PPM'].max(), 200)
kde = stats.gaussian_kde(df['PPM'])
kde_y = kde(kde_x)

# Plot KDE
plt.plot(kde_x, kde_y, color='red', linewidth=2.5, label='KDE (Bell Curve)')

# Add mean and median lines
plt.axvline(df['PPM'].mean(), color='red', linestyle='--', linewidth=1.5, alpha=0.7, label=f"Mean: {df['PPM'].mean():.3f}")
plt.axvline(df['PPM'].median(), color='green', linestyle='--', linewidth=1.5, alpha=0.7, label=f"Median: {df['PPM'].median():.3f}")

plt.xlabel('Points Per Minute (PPM)')
plt.ylabel('Density')
plt.title('Distribution of Player Efficiency (PPM) with Bell Curve')

# Add colorbar for reference
sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=df['PPM'].min(), vmax=df['PPM'].max()))
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.8)
cbar.set_label('PPM Value')

plt.legend()

# Add annotation for skewness
skewness = df['PPM'].skew()
if abs(skewness) < 0.5:
    shape_note = "📊 Approximately normal distribution"
elif skewness > 0:
    shape_note = f"📈 Right-skewed (tail towards high efficiency) — skewness = {skewness:.2f}"
else:
    shape_note = f"📉 Left-skewed (tail towards low efficiency) — skewness = {skewness:.2f}"

plt.annotate(shape_note, xy=(0.02, 0.95), xycoords='axes fraction', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

plt.tight_layout()
plt.savefig('../outputs/ppm_distribution.png', dpi=150)
plt.close()
print("   ✅ Saved: ppm_distribution.png (gradient colors + KDE bell curve)")

print("\n" + "=" * 60)
print("✅ STEP 4 COMPLETE!")
print("=" * 60)
print("\n📁 Outputs saved to /outputs folder:")
print("   1. correlation_comparison.png")
print("   2. top_teams_by_points.png")
print("   3. top_teams_efficiency.png")
print("   4. best_player_per_team.png")
print("   5. best_player_efficiency.png")
print("   6. top10_scorers.png (NOW uses team colors)")
print("   7. scatter_by_position.png")
print("   8. boxplot_by_position.png")
print("   9. teams_top100_scorers.png")
print("   10. ppm_distribution.png")