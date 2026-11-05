"""
Manufacturing Operations & Predictive Maintenance Analytics
Master Pipeline Execution Script
Runs all data cleaning, EDA, SQL database generation, financial analysis,
predictive modeling, and Power BI data prep in sequence.
"""

import subprocess
import sys
import time

SCRIPTS = [
    ("01: Data Ingestion & Cleaning", "notebooks_and_scripts/01_data_cleaning.py"),
    ("02: Exploratory Data Analysis & Visualizations", "notebooks_and_scripts/02_eda_analysis.py"),
    ("03: SQLite Database & SQL Queries", "notebooks_and_scripts/03_sql_analysis.py"),
    ("04: Financial Impact & Scenario Modeling", "notebooks_and_scripts/04_financial_impact.py"),
    ("05: Predictive Maintenance Machine Learning", "notebooks_and_scripts/05_predictive_maintenance.py"),
    ("06: Power BI Star Schema Data Prep", "notebooks_and_scripts/06_powerbi_data_prep.py"),
    ("07: Dashboard Architecture Preview", "create_dashboard_preview.py")
]

def main():
    print("=" * 80)
    print("DAIKIBO INDUSTRIALS: END-TO-END DATA ANALYTICS PIPELINE")
    print("=" * 80)
    start_total = time.time()
    
    for label, script_path in SCRIPTS:
        print(f"\n>>> Running Pipeline Module: {label} ({script_path})")
        t0 = time.time()
        ret = subprocess.run([sys.executable, script_path])
        elapsed = time.time() - t0
        if ret.returncode != 0:
            print(f"Error executing {script_path}. Pipeline aborted.")
            sys.exit(ret.returncode)
        print(f"Module completed successfully in {elapsed:.2f} seconds.")
        
    total_time = time.time() - start_total
    print("\n" + "=" * 80)
    print(f"FULL PIPELINE EXECUTION COMPLETED SUCCESSFULLY IN {total_time:.2f} SECONDS!")
    print("=" * 80)

if __name__ == "__main__":
    main()

