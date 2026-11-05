"""
Manufacturing Operations & Predictive Maintenance Analytics
Script 03: SQL Database Setup, Analytical Queries & Validation
Author: Senior Data Analyst & BI Consultant
"""

import sqlite3
import pandas as pd
import os

DB_PATH = "sql/daikibo_analytics.db"

def run_sql_analysis():
    print("=" * 80)
    print("STEP 3: SQL DATABASE SETUP & ANALYTICAL QUERIES")
    print("=" * 80)
    
    # 1. Load data
    df_clean = pd.read_csv("data/processed/daikibo_telemetry_clean.csv")
    df_incidents = pd.read_csv("data/processed/downtime_incidents.csv")
    df_daily = pd.read_csv("data/processed/factory_daily_summary.csv")
    df_machines = pd.read_csv("data/processed/machine_health_summary.csv")
    
    # 2. Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to SQLite database: {DB_PATH}")
    
    # Write tables
    print("Writing tables to SQLite...")
    df_clean.to_sql("fact_telemetry", conn, if_exists="replace", index=False)
    df_incidents.to_sql("fact_incidents", conn, if_exists="replace", index=False)
    df_daily.to_sql("fact_daily_summary", conn, if_exists="replace", index=False)
    df_machines.to_sql("dim_machines", conn, if_exists="replace", index=False)
    
    # Create indexes for optimal analytical query performance
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_factory ON fact_telemetry(factory_code);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_device ON fact_telemetry(device_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_status ON fact_telemetry(status);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_day ON fact_telemetry(day_of_month);")
    conn.commit()
    print("-> Tables and performance indexes created.")
    
    # -------------------------------------------------------------
    # SQL QUERY 1: FACTORIES EXPERIENCING THE HIGHEST DOWNTIME
    # -------------------------------------------------------------
    q1 = """
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
    """
    
    print("\n--- SQL Query 1: Factory Downtime Ranking ---")
    res1 = pd.read_sql_query(q1, conn)
    print(res1.to_string(index=False))
    
    # -------------------------------------------------------------
    # SQL QUERY 2: MACHINE TYPES WITH THE MOST FAILURES & DOWNTIME
    # -------------------------------------------------------------
    q2 = """
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
    """
    
    print("\n--- SQL Query 2: Machine Types With Most Failures ---")
    res2 = pd.read_sql_query(q2, conn)
    print(res2.to_string(index=False))
    
    # -------------------------------------------------------------
    # SQL QUERY 3: TOTAL UNHEALTHY MACHINE EVENTS AUDIT
    # -------------------------------------------------------------
    q3 = """
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
    """
    
    print("\n--- SQL Query 3: Status Breakdown & Unhealthy Events ---")
    res3 = pd.read_sql_query(q3, conn)
    print(res3.to_string(index=False))
    
    # -------------------------------------------------------------
    # SQL QUERY 4: FACTORY-WISE OPERATIONAL PERFORMANCE MATRIX
    # -------------------------------------------------------------
    q4 = """
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
    """
    
    print("\n--- SQL Query 4: Machines Experiencing Downtime ---")
    res4 = pd.read_sql_query(q4, conn)
    print(res4.to_string(index=False))
    
    # -------------------------------------------------------------
    # SQL QUERY 5: SHIFT AND TEMPORAL PATTERNS
    # -------------------------------------------------------------
    q5 = """
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
    """
    
    print("\n--- SQL Query 5: Shift Performance Breakdown ---")
    res5 = pd.read_sql_query(q5, conn)
    print(res5.to_string(index=False))
    
    # Save standalone SQL files
    os.makedirs("sql", exist_ok=True)
    with open("sql/01_factory_downtime_ranking.sql", "w") as f:
        f.write(q1.strip())
    with open("sql/02_machine_type_failures.sql", "w") as f:
        f.write(q2.strip())
    with open("sql/03_status_audit.sql", "w") as f:
        f.write(q3.strip())
    with open("sql/04_equipment_health_matrix.sql", "w") as f:
        f.write(q4.strip())
    with open("sql/05_shift_analysis.sql", "w") as f:
        f.write(q5.strip())
        
    # Write master SQL script
    master_sql = f"""/*
================================================================================
MANUFACTURING OPERATIONS & PREDICTIVE MAINTENANCE ANALYTICS
DAIKIBO TELEMETRY DATASET - COMPLETE SQL SUITE
Author: Senior Data Analyst & BI Consultant
================================================================================
*/

-- 1. FACTORY-LEVEL DOWNTIME & AVAILABILITY
{q1.strip()}

-- 2. EQUIPMENT TYPE FAILURE FREQUENCY & DOWNTIME
{q2.strip()}

-- 3. OVERALL SYSTEM STATUS AUDIT
{q3.strip()}

-- 4. EQUIPMENT REQUIRING OPERATIONAL ATTENTION
{q4.strip()}

-- 5. SHIFT-BASED BREAKDOWN ANALYSIS
{q5.strip()}
"""
    with open("sql/06_comprehensive_sql_suite.sql", "w") as f:
        f.write(master_sql)
        
    print("\nSuccessfully executed and exported all SQL queries to sql/ directory.")
    conn.close()

if __name__ == "__main__":
    run_sql_analysis()

