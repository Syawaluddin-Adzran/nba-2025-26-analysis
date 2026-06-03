import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from scipy import stats

# ---------- Page config ----------
st.set_page_config(
    page_title="NBA 2025-26 Analysis",
    page_icon="🏀",
    layout="wide"
)


# ---------- Create consistent team color map ----------
def get_team_color_map(teams):
    """Create a consistent color map for all teams using a fixed palette"""
    # Use a large, distinct color palette
    colors = px.colors.qualitative.Pastel + px.colors.qualitative.Set1 + px.colors.qualitative.Set2
    color_map = {}
    for i, team in enumerate(sorted(teams)):
        color_map[team] = colors[i % len(colors)]
    return color_map


# ---------- Load data ----------
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'data', 'cleaned', 'nba_2025_26_cleaned.csv')
    csv_path = os.path.normpath(csv_path)

    df = pd.read_csv(csv_path)

    # Calculate PPM (Points per minute)
    df['PPM'] = df['PTS'] / df['MP']

    # Player label for dropdowns
    df['Player_Label'] = df['Player'] + " (" + df['Team'] + ")"

    return df


df = load_data()

# ---------- FILTER OUT FAKE TEAMS FOR TEAM ANALYSIS ----------
real_teams = df[~df['Team'].str.contains('TM', na=False)]

# Create consistent color map for all real teams
team_color_map = get_team_color_map(real_teams['Team'].unique())

# ---------- Sidebar filters ----------
st.sidebar.header("🔍 Filters")

# Team filter (using REAL teams only)
all_teams = sorted(real_teams['Team'].unique())
selected_teams = st.sidebar.multiselect(
    "Select Teams",
    all_teams,
    default=all_teams[:5] if len(all_teams) > 5 else all_teams
)

# Position filter
all_positions = sorted(df['Pos'].dropna().unique())
selected_positions = st.sidebar.multiselect(
    "Select Positions",
    all_positions,
    default=all_positions
)

# Minutes range filter
min_minutes = int(df['MP'].min())
max_minutes = int(df['MP'].max())
minutes_range = st.sidebar.slider(
    "Minutes Played Range",
    min_minutes, max_minutes,
    (min_minutes, max_minutes)
)

# Apply filters (using full df for player data)
filtered_df = df[
    (df['Team'].isin(selected_teams)) &
    (df['Pos'].isin(selected_positions)) &
    (df['MP'] >= minutes_range[0]) &
    (df['MP'] <= minutes_range[1])
    ]

# Also create filtered_real for team charts (excludes 2TM)
filtered_real = filtered_df[~filtered_df['Team'].str.contains('TM', na=False)]

# ---------- Header ----------
st.title("🏀 NBA 2025-26 Analysis")
st.markdown("*Complete statistical analysis of the 2025-26 NBA regular season*")

# ---------- Key metrics row ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Players", len(filtered_df))
with col2:
    st.metric("🏆 Total Points", f"{filtered_df['PTS'].sum():,.0f}")
with col3:
    st.metric("⭐ Avg PPM", f"{filtered_df['PPM'].mean():.3f}")
with col4:
    st.metric("🎯 Correlation (MP vs PTS)", f"{filtered_df['MP'].corr(filtered_df['PTS']):.3f}")

st.markdown("---")

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Top Scorers",
    "📈 Minutes vs Points",
    "⚡ Efficiency",
    "📊 PPM Distribution"
])

# ============================================
# TAB 1: Top Scorers
# ============================================
with tab1:
    top_n = st.selectbox("Number of top scorers", [5, 10, 20, 50], index=1)

    top_scorers = filtered_df.nlargest(top_n, 'PTS')[['Player', 'Team', 'Pos', 'PTS', 'PPM', 'MP']]

    st.dataframe(top_scorers, use_container_width=True)

    # Sort by points descending for the chart
    top_scorers_sorted = top_scorers.sort_values('PTS', ascending=False)

    fig = px.bar(
        top_scorers_sorted,
        x='Player',
        y='PTS',
        color='Team',
        color_discrete_map=team_color_map,
        title=f"Top {top_n} Scorers",
        text='PTS',
        height=500,
        category_orders={'Player': top_scorers_sorted['Player'].tolist()}
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2: Minutes vs Points (Scatter)
# ============================================
with tab2:
    fig = px.scatter(
        filtered_df,
        x='MP',
        y='PTS',
        color='Pos',
        size='PPM',
        hover_name='Player',
        title="Minutes vs Points (size = Points Per Minute)",
        labels={'MP': 'Minutes Played', 'PTS': 'Total Points'},
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    # Correlation explanation
    corr = filtered_df['MP'].corr(filtered_df['PTS'])
    st.info(f"📈 **Correlation between minutes and points:** {corr:.3f}")
    st.caption(
        "A low correlation (<0.3) indicates that minutes played alone does not predict scoring – efficiency matters more.")

# ============================================
# TAB 3: EFFICIENCY (Player + Team)
# ============================================
with tab3:
    st.subheader("🏆 Player Efficiency")
    st.caption("Points Per Minute (PPM) – measures scoring efficiency regardless of playing time")

    col1, col2 = st.columns(2)

    with col1:
        # PPM by position (bar chart)
        pos_eff = filtered_df.groupby('Pos')['PPM'].mean().reset_index().sort_values('PPM', ascending=False)
        fig = px.bar(
            pos_eff,
            x='Pos',
            y='PPM',
            color='Pos',
            title="Average PPM by Position",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # PPM by position (box plot)
        fig = px.box(
            filtered_df,
            x='Pos',
            y='PPM',
            color='Pos',
            title="PPM Distribution by Position",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    # Most efficient players (min 500 minutes)
    st.subheader("Most Efficient Players (min 500 minutes)")
    high_minutes = filtered_df[filtered_df['MP'] > 500]
    top_efficient = high_minutes.nlargest(10, 'PPM')[['Player', 'Team', 'Pos', 'PPM', 'PTS', 'MP']]

    fig = px.bar(
        top_efficient,
        x='Player',
        y='PPM',
        color='Team',
        color_discrete_map=team_color_map,
        title="Top 10 Most Efficient Players",
        text='PPM',
        height=450
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Divider
    st.markdown("---")

    # Team Efficiency Section
    st.subheader("🏢 Team Efficiency")
    st.caption("Excludes 2TM, 3TM, 4TM (multi-team placeholder codes)")

    team_eff = filtered_real.groupby('Team')['PPM'].mean().reset_index().sort_values('PPM', ascending=False)

    if len(team_eff) > 0:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                team_eff.head(10),
                x='Team',
                y='PPM',
                color='Team',
                color_discrete_map=team_color_map,
                title="Top 10 Most Efficient Teams",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Team total points (for context)
            team_points = filtered_real.groupby('Team')['PTS'].sum().reset_index().sort_values('PTS',
                                                                                               ascending=False).head(10)
            fig = px.bar(
                team_points,
                x='Team',
                y='PTS',
                color='Team',
                color_discrete_map=team_color_map,
                title="Top 10 Teams by Total Points",
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)

        # Team efficiency table
        with st.expander("View All Teams (Sorted by Efficiency)"):
            st.dataframe(team_eff.sort_values('PPM', ascending=False), use_container_width=True)

    else:
        st.info("No real team data available with current filters")

# ============================================
# TAB 4: PPM Distribution (Bell Curve)
# ============================================
with tab4:
    st.subheader("PPM Distribution Across the League")
    st.caption("Shows how player efficiency is distributed – a bell curve indicates normal distribution")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Histogram with KDE
        fig = go.Figure()

        # Add histogram
        fig.add_trace(go.Histogram(
            x=filtered_df['PPM'],
            nbinsx=30,
            name='Players',
            opacity=0.7,
            marker_color='steelblue'
        ))

        # Add KDE (bell curve)
        kde_x = np.linspace(filtered_df['PPM'].min(), filtered_df['PPM'].max(), 100)
        kde = stats.gaussian_kde(filtered_df['PPM'])
        kde_y = kde(kde_x)
        # Scale KDE to match histogram
        hist_counts, bin_edges = np.histogram(filtered_df['PPM'], bins=30)
        scale_factor = max(hist_counts) / max(kde_y) if max(kde_y) > 0 else 1
        fig.add_trace(go.Scatter(
            x=kde_x,
            y=kde_y * scale_factor,
            mode='lines',
            name='Bell Curve (KDE)',
            line=dict(color='red', width=2)
        ))

        fig.update_layout(
            title="Distribution of Points Per Minute (PPM)",
            xaxis_title="PPM",
            yaxis_title="Number of Players",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Summary statistics
        st.metric("Mean PPM", f"{filtered_df['PPM'].mean():.3f}")
        st.metric("Median PPM", f"{filtered_df['PPM'].median():.3f}")
        st.metric("Std Dev", f"{filtered_df['PPM'].std():.3f}")
        st.metric("Skewness", f"{filtered_df['PPM'].skew():.3f}")

        skew = filtered_df['PPM'].skew()
        if abs(skew) < 0.5:
            st.success("📊 Distribution is approximately normal (bell curve)")
        elif skew > 0:
            st.warning(f"📊 Distribution is right-skewed (tail towards high efficiency) — skewness = {skew:.2f}")
        else:
            st.warning(f"📊 Distribution is left-skewed (tail towards low efficiency) — skewness = {skew:.2f}")

# ---------- Footer ----------
st.markdown("---")
st.caption("📊 Data source: Basketball Reference | Built with Streamlit, Pandas, Plotly")
st.caption("🎯 Analysis: Minutes vs Points | Player & Team Efficiency | PPM Distribution")
st.caption("🚫 Note: Team analysis excludes 2TM, 3TM, 4TM (multi-team placeholder codes)")