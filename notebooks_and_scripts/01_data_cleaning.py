"""
Manufacturing Operations & Predictive Maintenance Analytics
Script 01: Data Collection, Ingestion, Quality Validation & Cleaning
Author: Senior Data Analyst & BI Consultant
"""

import json
import os
import pandas as pd
import numpy as np

def run_data_cleaning():
    print("=" * 80)
    print("STEP 1: DATA INGESTION & QUALITY VALIDATION")
    print("=" * 80)
    
    raw_json_path = "data/raw/extracted/daikibo-telemetry-data.json"
    if not os.path.exists(raw_json_path):
        raise FileNotFoundError(f"Source file not found at {raw_json_path}")
        
    print(f"Loading raw telemetry JSON from: {raw_json_path}...")
    with open(raw_json_path, "r") as f:
        raw_data = json.load(f)
        
    raw_record_count = len(raw_data)
    print(f"-> Successfully loaded {raw_record_count:,} raw telemetry records.")
    
    # Flatten nested JSON
    df_raw = pd.json_normalize(raw_data)
    print(f"-> Normalized DataFrame shape: {df_raw.shape}")
    print(f"-> Raw columns: {list(df_raw.columns)}")
    
    # Validation checks
    null_counts = df_raw.isnull().sum()
    print("\nNull Value Audit:")
    for col, count in null_counts.items():
        print(f"   - {col}: {count} nulls")
        
    # Standardize column names
    col_mapping = {
        "deviceID": "device_id",
        "deviceType": "device_type",
        "timestamp": "raw_timestamp",
        "location.country": "country_raw",
        "location.city": "city_raw",
        "location.area": "area_raw",
        "location.factory": "factory_raw",
        "location.section": "section_raw",
        "data.status": "status_raw",
        "data.temperature": "temperature_c"
    }
    df = df_raw.rename(columns=col_mapping)
    
    # Clean string fields & title casing
    df["country"] = df["country_raw"].str.strip().str.title()
    df["city"] = df["city_raw"].str.strip().str.title()
    df["area"] = df["area_raw"].str.replace("-", " ").str.title()
    df["section"] = df["section_raw"].str.replace("-", " ").str.title()
    
    factory_display_map = {
        "daikibo-factory-meiyo": "Factory Meiyo (Tokyo)",
        "daikibo-factory-seiko": "Factory Seiko (Osaka)",
        "daikibo-berlin": "Berlin Facility (Germany)",
        "daikibo-shenzhen": "Shenzhen Plant (China)"
    }
    factory_code_map = {
        "daikibo-factory-meiyo": "FAC-TYO-01",
        "daikibo-factory-seiko": "FAC-OSA-02",
        "daikibo-berlin": "FAC-BER-03",
        "daikibo-shenzhen": "FAC-SZX-04"
    }
    df["factory_name"] = df["factory_raw"].map(factory_display_map)
    df["factory_code"] = df["factory_raw"].map(factory_code_map)
    
    # Status standardization
    df["status"] = df["status_raw"].str.strip().str.title()
    df["is_unhealthy"] = (df["status"] == "Unhealthy").astype(int)
    # Deloitte simulation business rule: each telemetry interval is 10 minutes
    df["downtime_minutes"] = df["is_unhealthy"] * 10
    
    # Datetime handling
    df["datetime_utc"] = pd.to_datetime(df["raw_timestamp"], unit="ms")
    df["date"] = df["datetime_utc"].dt.date
    df["time"] = df["datetime_utc"].dt.time
    df["hour"] = df["datetime_utc"].dt.hour
    
    # Operational Shift Assignment:
    # Shift 1 (Morning): 06:00 - 14:00
    # Shift 2 (Afternoon/Evening): 14:00 - 22:00
    # Shift 3 (Night): 22:00 - 06:00
    conditions = [
        (df["hour"] >= 6) & (df["hour"] < 14),
        (df["hour"] >= 14) & (df["hour"] < 22)
    ]
    choices = ["Shift 1 (Morning)", "Shift 2 (Afternoon)"]
    df["shift"] = np.select(conditions, choices, default="Shift 3 (Night)")
    
    # Batch & Daily simulation mapping
    # 124 blocks of 1,296 records = 4 factories * 31 daily simulation iterations
    df["block_id"] = df.index // 1296
    df["day_of_month"] = (df["block_id"] % 31) + 1
    
    print("\nOperational Status Summary:")
    print(df["status"].value_counts())
    print(f"Total recorded downtime: {df['downtime_minutes'].sum():,} minutes ({df['downtime_minutes'].sum()/60:.2f} hours)")
    
    # Rearrange final clean columns
    clean_cols = [
        "device_id", "device_type", "factory_code", "factory_name", "country", "city",
        "area", "section", "raw_timestamp", "datetime_utc", "date", "time", "hour",
        "shift", "block_id", "day_of_month", "status", "is_unhealthy", "downtime_minutes",
        "temperature_c"
    ]
    df_clean = df[clean_cols]
    
    # Save cleaned telemetry dataset
    output_clean_csv = "data/processed/daikibo_telemetry_clean.csv"
    print(f"\nSaving cleaned telemetry to: {output_clean_csv}...")
    df_clean.to_csv(output_clean_csv, index=False)
    print(f"-> Successfully written {len(df_clean):,} records.")
    
    # -------------------------------------------------------------
    # STEP 2: INCIDENT EXTRACTION (Grouping consecutive outages)
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 2: EXTRACTING FAILURE INCIDENTS (EPISODES)")
    print("=" * 80)
    
    # Filter unhealthy events
    unhealthy_events = df_clean[df_clean["is_unhealthy"] == 1].copy()
    unhealthy_events = unhealthy_events.sort_values(["device_id", "block_id", "datetime_utc"])
    
    # Identify contiguous blocks
    # An incident ends if block_id changes, or time difference > 10 minutes
    unhealthy_events["prev_block"] = unhealthy_events["block_id"].shift(1)
    unhealthy_events["prev_time"] = unhealthy_events["datetime_utc"].shift(1)
    unhealthy_events["prev_dev"] = unhealthy_events["device_id"].shift(1)
    
    unhealthy_events["time_gap_mins"] = (unhealthy_events["datetime_utc"] - unhealthy_events["prev_time"]).dt.total_seconds() / 60.0
    
    # New incident flag
    is_new_incident = (
        (unhealthy_events["device_id"] != unhealthy_events["prev_dev"]) |
        (unhealthy_events["block_id"] != unhealthy_events["prev_block"]) |
        (unhealthy_events["time_gap_mins"] > 10.0)
    )
    unhealthy_events["incident_group"] = is_new_incident.cumsum()
    
    incidents = []
    for inc_id, group in unhealthy_events.groupby("incident_group"):
        first_row = group.iloc[0]
        last_row = group.iloc[-1]
        
        events_count = len(group)
        duration_mins = events_count * 10
        avg_temp = group["temperature_c"].mean()
        
        # Determine failure category
        if duration_mins >= 240:
            severity = "Catastrophic (Critical Outage > 4 hrs)"
        elif duration_mins >= 60:
            severity = "Major Breakdown (1 - 4 hrs)"
        else:
            severity = "Minor Interruption (< 1 hr)"
            
        incidents.append({
            "incident_id": f"INC-{inc_id:03d}",
            "device_id": first_row["device_id"],
            "device_type": first_row["device_type"],
            "factory_code": first_row["factory_code"],
            "factory_name": first_row["factory_name"],
            "country": first_row["country"],
            "city": first_row["city"],
            "section": first_row["section"],
            "block_id": int(first_row["block_id"]),
            "day_of_month": int(first_row["day_of_month"]),
            "shift": first_row["shift"],
            "start_time": first_row["datetime_utc"],
            "end_time": last_row["datetime_utc"] + pd.Timedelta(minutes=10),
            "unhealthy_event_count": events_count,
            "downtime_minutes": duration_mins,
            "downtime_hours": round(duration_mins / 60.0, 2),
            "avg_temperature_c": round(avg_temp, 1),
            "severity_classification": severity
        })
        
    df_incidents = pd.DataFrame(incidents)
    incidents_path = "data/processed/downtime_incidents.csv"
    df_incidents.to_csv(incidents_path, index=False)
    print(f"-> Extracted {len(df_incidents)} distinct failure incidents.")
    print(f"-> Saved incident log to: {incidents_path}")
    print("\nIncident Summary by Severity:")
    print(df_incidents["severity_classification"].value_counts())
    
    # -------------------------------------------------------------
    # STEP 3: AGGREGATE SUMMARY TABLES
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 3: COMPUTING AGGREGATE OPERATIONAL SUMMARIES")
    print("=" * 80)
    
    # Factory Daily Summary
    daily_summary = df_clean.groupby(
        ["factory_code", "factory_name", "country", "city", "day_of_month"]
    ).agg(
        total_readings=("device_id", "count"),
        healthy_readings=("status", lambda x: (x == "Healthy").sum()),
        unhealthy_readings=("status", lambda x: (x == "Unhealthy").sum()),
        downtime_minutes=("downtime_minutes", "sum"),
        avg_temperature=("temperature_c", "mean")
    ).reset_index()
    
    daily_summary["downtime_hours"] = daily_summary["downtime_minutes"] / 60.0
    daily_summary["planned_production_minutes"] = daily_summary["total_readings"] * 10
    daily_summary["operating_availability_pct"] = (
        (daily_summary["planned_production_minutes"] - daily_summary["downtime_minutes"]) / 
        daily_summary["planned_production_minutes"]
    ) * 100.0
    
    daily_summary_path = "data/processed/factory_daily_summary.csv"
    daily_summary.to_csv(daily_summary_path, index=False)
    print(f"-> Saved factory daily summary to: {daily_summary_path}")
    
    # Machine Health Summary
    machine_summary = df_clean.groupby(
        ["device_id", "device_type", "factory_code", "factory_name", "section"]
    ).agg(
        total_telemetry_cycles=("status", "count"),
        healthy_cycles=("status", lambda x: (x == "Healthy").sum()),
        unhealthy_cycles=("status", lambda x: (x == "Unhealthy").sum()),
        total_downtime_mins=("downtime_minutes", "sum"),
        avg_temp=("temperature_c", "mean"),
        max_temp=("temperature_c", "max"),
        min_temp=("temperature_c", "min")
    ).reset_index()
    
    machine_summary["total_downtime_hours"] = machine_summary["total_downtime_mins"] / 60.0
    machine_summary["availability_pct"] = (
        machine_summary["healthy_cycles"] / machine_summary["total_telemetry_cycles"]
    ) * 100.0
    
    # Count incidents per machine
    inc_counts = df_incidents.groupby("device_id")["incident_id"].count().reset_index()
    inc_counts = inc_counts.rename(columns={"incident_id": "total_failure_incidents"})
    machine_summary = machine_summary.merge(inc_counts, on="device_id", how="left")
    machine_summary["total_failure_incidents"] = machine_summary["total_failure_incidents"].fillna(0).astype(int)
    
    # Mean Time Between Failures (MTBF) and Mean Time To Repair (MTTR)
    # Total operational operating time (hours) = total_cycles * 10 / 60 - downtime_hours
    machine_summary["operating_hours"] = (machine_summary["total_telemetry_cycles"] * 10 / 60.0) - machine_summary["total_downtime_hours"]
    
    machine_summary["mtbf_hours"] = np.where(
        machine_summary["total_failure_incidents"] > 0,
        machine_summary["operating_hours"] / machine_summary["total_failure_incidents"],
        machine_summary["operating_hours"] # No failures
    )
    
    machine_summary["mttr_minutes"] = np.where(
        machine_summary["total_failure_incidents"] > 0,
        machine_summary["total_downtime_mins"] / machine_summary["total_failure_incidents"],
        0.0
    )
    
    # Machine Health Index (0 - 100)
    # Weighted by availability and MTTR penalty
    machine_summary["health_score"] = np.clip(
        machine_summary["availability_pct"] - (machine_summary["total_failure_incidents"] * 0.5),
        0.0, 100.0
    )
    
    machine_path = "data/processed/machine_health_summary.csv"
    machine_summary.to_csv(machine_path, index=False)
    print(f"-> Saved machine health summary to: {machine_path}")
    
    print("\nData Cleaning & Preparation Phase Successfully Completed!")

if __name__ == "__main__":
    run_data_cleaning()

