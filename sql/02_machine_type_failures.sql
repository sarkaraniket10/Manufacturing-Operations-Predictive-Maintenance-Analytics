-- Query 2: Machine Types Failure Frequency, Total Downtime, and Incident Count
    SELECT 
        t.device_type,
        COUNT(DISTINCT t.device_id) AS total_active_machines,
        COUNT(*) AS total_telemetry_records,
        SUM(CASE WHEN t.status = 'Unhealthy' THEN 1 ELSE 0 END) AS total_unhealthy_events,
        SUM(t.downtime_minutes) AS total_downtime_minutes,
        ROUND(SUM(t.downtime_minutes) / 60.0, 2) AS total_downtime_hours,
        COALESCE(COUNT(DISTINCT i.incident_id), 0) AS failure_incident_count,
        ROUND(AVG(t.temperature_c), 2) AS avg_operational_temp_c,
        ROUND((SUM(t.downtime_minutes) * 100.0) / SUM(SUM(t.downtime_minutes)) OVER(), 2) AS pct_of_total_downtime,
        RANK() OVER (ORDER BY SUM(t.downtime_minutes) DESC) AS machine_downtime_rank
    FROM fact_telemetry t
    LEFT JOIN fact_incidents i 
        ON t.device_type = i.device_type 
        AND t.factory_code = i.factory_code
        AND t.day_of_month = i.day_of_month
    GROUP BY t.device_type
    ORDER BY total_downtime_minutes DESC;