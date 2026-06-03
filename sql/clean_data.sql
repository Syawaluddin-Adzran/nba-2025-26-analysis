-- ============================================
-- 1. Create cleaned_players table
-- ============================================

CREATE TABLE IF NOT EXISTS cleaned_players AS

SELECT
    -- Core identity
    Player,
    Team,
    MAX(Pos) AS Position,
    MAX(Age) AS Age,

    -- Summed stats (for multi-team players)
    SUM(MP) AS Minutes,
    SUM(PTS) AS Points,

    -- Handle NULL percentages (use double quotes for special names)
    AVG(CASE WHEN "FG%" IS NOT NULL THEN "FG%" END) AS FG_Pct,
    AVG(CASE WHEN "3P%" IS NOT NULL THEN "3P%" END) AS ThreeP_Pct,
    AVG(CASE WHEN "FT%" IS NOT NULL THEN "FT%" END) AS FT_Pct,

    -- Calculated efficiency
    SUM(PTS) * 1.0 / SUM(MP) AS PPM

FROM raw_players

GROUP BY Player;

-- ============================================
-- 2. Remove rows with missing critical data
-- ============================================

DELETE FROM cleaned_players
WHERE Minutes IS NULL OR Points IS NULL;

-- ============================================
-- 3. Add indexes for faster queries
-- ============================================

CREATE INDEX IF NOT EXISTS idx_team ON cleaned_players(Team);
CREATE INDEX IF NOT EXISTS idx_position ON cleaned_players(Position);
CREATE INDEX IF NOT EXISTS idx_ppm ON cleaned_players(PPM DESC);

-- ============================================
-- 4. Final check: show row counts
-- ============================================

SELECT 'raw_players' AS table_name, COUNT(*) AS row_count FROM raw_players
UNION ALL
SELECT 'cleaned_players', COUNT(*) FROM cleaned_players;