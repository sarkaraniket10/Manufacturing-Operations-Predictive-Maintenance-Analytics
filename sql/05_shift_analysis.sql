-- Query 5: Operational Shift Downtime Analysis
    SELECT 
        shift,
        COUNT(*) AS telemetry_records,
        SUM(CASE WHEN status = 'Unhealthy' THEN 1 ELSE 0 END) AS unhealthy_events,
        SUM(downtime_minutes) AS downtime_minutes,
        ROUND(SUM(downtime_minutes) / 60.0, 2) AS downtime_hours,
        ROUND((SUM(downtime_minutes) * 100.0) / (SELECT SUM(downtime_minutes) FROM fact_telemetry), 2) AS shift_downtime_share_pct
    FROM fact_telemetry
    GROUP BY shift
    ORDER BY downtime_minutes DESC;