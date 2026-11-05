-- Query 3: Total Unhealthy Telemetry Events Audit Across System
    SELECT 
        status,
        COUNT(*) AS event_count,
        ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM fact_telemetry), 4) AS event_percentage,
        SUM(downtime_minutes) AS downtime_minutes_recorded,
        ROUND(SUM(downtime_minutes) / 60.0, 2) AS downtime_hours_recorded
    FROM fact_telemetry
    GROUP BY status
    ORDER BY event_count DESC;