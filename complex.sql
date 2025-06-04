WITH WinePerformance AS (
    SELECT
        name, region, variety,
        CAST(substr(name, length(name) - 3, 4) AS INTEGER) AS wine_year,  -- Extract the year from the name
        rating, notes
    FROM wines
),
RollingAvg AS (
    SELECT
        region, variety, wine_year,
        AVG(rating) OVER (PARTITION BY region, variety ORDER BY wine_year ROWS BETWEEN 600 PRECEDING AND CURRENT ROW) AS rolling_avg_rating
    FROM WinePerformance
),
TopRegions AS (
    SELECT region
    FROM (
        SELECT region, COUNT(*) AS wine_count
        FROM WinePerformance
        GROUP BY region
        ORDER BY wine_count DESC
        LIMIT 15
    ) tr
)
SELECT
    wp.name, wp.region, wp.variety, wp.wine_year, wp.rating, ra.rolling_avg_rating,
    ROUND(wp.rating * 1000 / (ra.rolling_avg_rating + 1), 2) AS performance_ratio,
    CASE
        WHEN wp.rating > ra.rolling_avg_rating THEN 'Above Rolling Avg'
        WHEN wp.rating = ra.rolling_avg_rating THEN 'Equal to Rolling Avg'
        ELSE 'Below Rolling Avg'
    END AS performance_trend,
    CASE
        WHEN wp.rating < 50 THEN 'Low Rating'
        WHEN wp.rating BETWEEN 50 AND 75 THEN 'Medium Rating'
        ELSE 'High Rating'
    END AS rating_category
FROM WinePerformance wp
JOIN RollingAvg ra
    ON wp.region = ra.region AND wp.variety = ra.variety AND wp.wine_year = ra.wine_year
WHERE wp.region IN (SELECT region FROM TopRegions) AND wp.rating > 50
ORDER BY wp.region, wp.variety, wp.wine_year DESC, LENGTH(wp.name) DESC
LIMIT 50;