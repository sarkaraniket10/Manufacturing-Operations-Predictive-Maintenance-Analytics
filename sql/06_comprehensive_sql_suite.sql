/*
================================================================================
MANUFACTURING OPERATIONS & PREDICTIVE MAINTENANCE ANALYTICS
DAIKIBO TELEMETRY DATASET - COMPLETE SQL SUITE
Author: Senior Data Analyst & BI Consultant
================================================================================
*/

-- 1. FACTORY-LEVEL DOWNTIME & AVAILABILITY
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

-- 2. EQUIPMENT TYPE FAILURE FREQUENCY & DOWNTIME
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

-- 3. OVERALL SYSTEM STATUS AUDIT
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

-- 4. EQUIPMENT REQUIRING OPERATIONAL ATTENTION
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

-- 5. SHIFT-BASED BREAKDOWN ANALYSIS
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
