-- Query 1: Factory Downtime Ranking, Availability and Share of Total Outage
    WITH TotalGlobalDowntime AS (
        SELECT SUM(downtime_minutes) AS global_downtime_mins
        FROM fact_telemetry
    )
    SELECT 
        factory_code,
        factory_name,
        country,
        city,
        COUNT(*) AS total_telemetry_events,
        SUM(CASE WHEN status = 'Unhealthy' THEN 1 ELSE 0 END) AS unhealthy_events,
        SUM(downtime_minutes) AS total_downtime_minutes,
        ROUND(SUM(downtime_minutes) / 60.0, 2) AS total_downtime_hours,
        ROUND((1.0 - (CAST(SUM(downtime_minutes) AS FLOAT) / (COUNT(*) * 10.0))) * 100.0, 4) AS operational_availability_pct,
        ROUND((CAST(SUM(downtime_minutes) AS FLOAT) / (SELECT global_downtime_mins FROM TotalGlobalDowntime)) * 100.0, 2) AS pct_of_global_downtime,
        DENSE_RANK() OVER (ORDER BY SUM(downtime_minutes) DESC) AS downtime_rank
    FROM fact_telemetry
    GROUP BY factory_code, factory_name, country, city
    ORDER BY total_downtime_minutes DESC;