"""
Manufacturing Operations & Predictive Maintenance Analytics
Script 06: Power BI Data Model Preparation & Dimension/Fact Extraction
Author: Senior Data Analyst & BI Consultant
"""

import os
import pandas as pd
import numpy as np

def run_powerbi_prep():
    print("=" * 80)
    print("STEP 6: PREPARING POWER BI STAR SCHEMA DATASETS")
    print("=" * 80)
    
    os.makedirs("data/powerbi", exist_ok=True)
    
    # Load processed data
    df = pd.read_csv("data/processed/daikibo_telemetry_clean.csv")
    incidents = pd.read_csv("data/processed/downtime_incidents.csv")
    
    # -------------------------------------------------------------
    # 1. DIM_FACTORY
    # -------------------------------------------------------------
    factory_geo = {
        "FAC-TYO-01": {"lat": 35.6762, "lon": 139.6503, "headcount": 450},
        "FAC-OSA-02": {"lat": 34.6937, "lon": 135.5023, "headcount": 380},
        "FAC-BER-03": {"lat": 52.5200, "lon": 13.4050, "headcount": 290},
        "FAC-SZX-04": {"lat": 22.5431, "lon": 114.0579, "headcount": 620}
    }
    
    dim_factory = df[["factory_code", "factory_name", "country", "city", "area"]].drop_duplicates().reset_index(drop=True)
    dim_factory["latitude"] = dim_factory["factory_code"].map(lambda x: factory_geo[x]["lat"])
    dim_factory["longitude"] = dim_factory["factory_code"].map(lambda x: factory_geo[x]["lon"])
    dim_factory["plant_workforce"] = dim_factory["factory_code"].map(lambda x: factory_geo[x]["headcount"])
    dim_factory["operating_status"] = "Active 24/7"
    
    dim_factory.to_csv("data/powerbi/dim_factory.csv", index=False)
    print(f"-> Generated dim_factory.csv ({len(dim_factory)} rows)")
    
    # -------------------------------------------------------------
    # 2. DIM_MACHINE
    # -------------------------------------------------------------
    criticality_map = {
        "LaserWelder": "Tier 1 - Critical High Revenue",
        "LaserCutter": "Tier 1 - Critical High Revenue",
        "Furnace": "Tier 1 - Critical Process",
        "ConveyorBelt": "Tier 2 - Critical Flow Bottleneck",
        "CNC": "Tier 2 - High Precision",
        "HeavyDutyDrill": "Tier 2 - Structural Machining",
        "MetalPress": "Tier 2 - Stamping Capacity",
        "SpotWelder": "Tier 3 - Standard Assembly",
        "AirWrench": "Tier 3 - Manual Workstation"
    }
    
    dim_machine = df[["device_id", "device_type", "factory_code", "section"]].drop_duplicates().reset_index(drop=True)
    dim_machine["criticality_tier"] = dim_machine["device_type"].map(criticality_map)
    dim_machine["commission_year"] = np.random.choice([2018, 2019, 2020, 2021], size=len(dim_machine))
    dim_machine["maintenance_cycle_days"] = 30
    
    dim_machine.to_csv("data/powerbi/dim_machine.csv", index=False)
    print(f"-> Generated dim_machine.csv ({len(dim_machine)} rows)")
    
    # -------------------------------------------------------------
    # 3. DIM_MACHINE_TYPE
    # -------------------------------------------------------------
    category_map = {
        "LaserCutter": "Thermal & Optical Cutting",
        "LaserWelder": "Automated Fusion Joining",
        "Furnace": "Thermal Processing",
        "HeavyDutyDrill": "Mechanical Material Removal",
        "CNC": "Precision Computerized Machining",
        "SpotWelder": "Electrical Resistance Welding",
        "ConveyorBelt": "Automated Material Transfer",
        "MetalPress": "Sheet Stamping & Forming",
        "AirWrench": "Pneumatic Fastening"
    }
    
    dim_machine_type = pd.DataFrame([
        {"device_type": k, "equipment_category": v, "criticality": criticality_map[k]}
        for k, v in category_map.items()
    ])
    dim_machine_type.to_csv("data/powerbi/dim_machine_type.csv", index=False)
    print(f"-> Generated dim_machine_type.csv ({len(dim_machine_type)} rows)")
    
    # -------------------------------------------------------------
    # 4. DIM_DATE
    # -------------------------------------------------------------
    base_date = pd.to_datetime("2021-05-01")
    date_list = [base_date + pd.Timedelta(days=i) for i in range(31)]
    dim_date = pd.DataFrame({
        "date": [d.strftime("%Y-%m-%d") for d in date_list],
        "date_key": [int(d.strftime("%Y%m%d")) for d in date_list],
        "day_of_month": [d.day for d in date_list],
        "day_name": [d.strftime("%A") for d in date_list],
        "is_weekend": [1 if d.weekday() >= 5 else 0 for d in date_list],
        "week_number": [d.isocalendar()[1] for d in date_list],
        "month_name": "May",
        "year": 2021
    })
    dim_date.to_csv("data/powerbi/dim_date.csv", index=False)
    print(f"-> Generated dim_date.csv ({len(dim_date)} rows)")
    
    # -------------------------------------------------------------
    # 5. FACT_TELEMETRY_SUMMARY
    # (High performance aggregate table for fast Power BI loading)
    # -------------------------------------------------------------
    # Map simulation day_of_month to date in May 2021
    day_to_date_map = {d.day: d.strftime("%Y-%m-%d") for d in date_list}
    df["calendar_date"] = df["day_of_month"].map(day_to_date_map)
    
    fact_telemetry_summary = df.groupby(
        ["calendar_date", "day_of_month", "factory_code", "device_id", "shift"]
    ).agg(
        total_cycles=("status", "count"),
        healthy_cycles=("status", lambda x: (x == "Healthy").sum()),
        unhealthy_cycles=("status", lambda x: (x == "Unhealthy").sum()),
        downtime_minutes=("downtime_minutes", "sum"),
        avg_temperature_c=("temperature_c", "mean")
    ).reset_index()
    
    fact_telemetry_summary["downtime_hours"] = fact_telemetry_summary["downtime_minutes"] / 60.0
    fact_telemetry_summary["planned_operating_minutes"] = fact_telemetry_summary["total_cycles"] * 10
    fact_telemetry_summary["operating_availability_pct"] = (
        (fact_telemetry_summary["planned_operating_minutes"] - fact_telemetry_summary["downtime_minutes"]) / 
        fact_telemetry_summary["planned_operating_minutes"]
    ) * 100.0
    
    fact_telemetry_summary.to_csv("data/powerbi/fact_telemetry_summary.csv", index=False)
    print(f"-> Generated fact_telemetry_summary.csv ({len(fact_telemetry_summary)} rows)")
    
    # -------------------------------------------------------------
    # 6. FACT_DOWNTIME_INCIDENTS
    # -------------------------------------------------------------
    incidents["calendar_date"] = incidents["day_of_month"].map(day_to_date_map)
    incidents.to_csv("data/powerbi/fact_downtime_incidents.csv", index=False)
    print(f"-> Generated fact_downtime_incidents.csv ({len(incidents)} rows)")
    
    print("\nAll Power BI Star Schema Tables Successfully Exported to data/powerbi/!")

if __name__ == "__main__":
    run_powerbi_prep()

