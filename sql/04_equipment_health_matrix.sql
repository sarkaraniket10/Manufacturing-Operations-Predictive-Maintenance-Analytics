-- Query 4: Cross-Factory Operational Reliability & Machine Health
    SELECT 
        factory_name,
        device_type,
        COUNT(*) AS total_cycles,
        SUM(CASE WHEN status = 'Unhealthy' THEN 1 ELSE 0 END) AS unhealthy_cycles,
        SUM(downtime_minutes) AS downtime_mins,
        ROUND((1.0 - (CAST(SUM(downtime_minutes) AS FLOAT) / (COUNT(*) * 10.0))) * 100.0, 3) AS availability_pct,
        CASE 
            WHEN SUM(downtime_minutes) = 0 THEN 'Optimal (100% Health)'
            WHEN SUM(downtime_minutes) <= 60 THEN 'Good (Low Downtime)'
            WHEN SUM(downtime_minutes) <= 200 THEN 'Moderate (Attention Required)'
            ELSE 'Critical (Immediate Action Required)'
        END AS equipment_health_status
    FROM fact_telemetry
    GROUP BY factory_name, device_type
    HAVING SUM(downtime_minutes) > 0
    ORDER BY downtime_mins DESC;