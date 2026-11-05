# Manufacturing Operations & Predictive Maintenance Analytics
### Global Telemetry Diagnostics, Equipment Reliability & Financial Risk Optimization
**Client Simulation:** Daikibo Industrials (Deloitte Australia Data Analytics Job Simulation)  
**Role:** Senior Data Analyst & Business Intelligence Consultant  
**Status:** Completed & Production Ready  

---

## Executive Summary

Modern discrete manufacturing operates on razor-thin throughput margins where unplanned equipment stoppages cascade into catastrophic financial losses, missed delivery service levels (SLAs), and expensive emergency maintenance overtime. 

This end-to-end data analytics and business intelligence project evaluates continuous industrial telemetry from **Daikibo Industrials**, a multinational heavy manufacturing enterprise operating four discrete production plants in **Tokyo (Factory Meiyo)**, **Osaka (Factory Seiko)**, **Berlin (Germany)**, and **Shenzhen (China)**.

Analyzing **160,704 sensor telemetry cycles** across **36 mission-critical manufacturing assets** over a 31-day operational period, this project uncovers two divergent failure archetypes:
1. **Catastrophic Acute Failure**: Factory Seiko suffered an uninterrupted **8.0-hour single breakdown** on its primary LaserWelder ($12,370 loss).
2. **Chronic Intermittent Micro-Stoppage (*Chokotei*)**: Shenzhen Plant suffered **21 distinct breakdown episodes** on its primary LaserCutter across 14 operational days, generating severe work-in-progress (WIP) scrap and racking up **$13,983 in financial losses** (the highest across the fleet).

Through multi-layer SQL analytics, machine learning predictive maintenance modeling (Random Forest ROC-AUC: **0.963**, PR-AUC: **0.520**), and an executive 4-page Microsoft Power BI dashboard suite, this project delivers five boardroom-ready recommendations projected to **reduce downtime by 75%** and capture **$247,426 in annualized net cost savings** (394.9% Year-1 ROI).

---

## Project Architecture & Methodology

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DAIKIBO TELEMETRY PIPELINE                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 1. DATA INGESTION, AUDIT & CLEANING                     │
       │ • 160,704 raw JSON records ingested                     │
       │ • Validation: 0 nulls, 103 unhealthy events flagged      │
       │ • 29 failure episodes consolidated with severity tags   │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 2. EXPLORATORY DATA ANALYSIS & VISUALIZATION            │
       │ • Factory downtime distribution (Seiko 480m, SZX 420m)  │
       │ • Machine type concentration (Lasers = 88.3% outage)    │
       │ • Diurnal shift analysis (Morning shift = 58.25%)       │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 3. ENTERPRISE SQL SUITE (SQLite / DuckDB)               │
       │ • High-performance window functions & rankings         │
       │ • MTBF & MTTR reliability metrics                       │
       │ • Equipment health score indexing                       │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 4. PREDICTIVE MAINTENANCE & FINANCIAL MODELING          │
       │ • Feature engineering: rolling volatility & cycle wear  │
       │ • Machine Learning: Random Forest (ROC-AUC 0.963)       │
       │ • Cost quantification: Throughput + Labor + Scrap       │
       │ • What-If ROI Simulation (Scenarios A, B, C)            │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │ 5. POWER BI ENTERPRISE DASHBOARD SUITE                  │
       │ • Star Schema: 4 Dimensions + 2 Fact Tables             │
       │ • 4 Analytical Pages (Executive, Factory, Machine, Risk)│
       │ • Dark Navy & Teal consulting design system             │
       └─────────────────────────────────────────────────────────┘
```

---

## Technology Stack

- **Data Processing & Engineering:** Python 3.11, Pandas, NumPy
- **Machine Learning & Feature Engineering:** Scikit-learn (Random Forest, Gradient Boosting, Logistic Regression)
- **Database & Query Optimization:** SQLite 3, SQL Window Functions (`DENSE_RANK()`, `SUM() OVER()`)
- **Exploratory Visualizations:** Matplotlib, Seaborn
- **Business Intelligence & Executive Reporting:** Microsoft Power BI Desktop (Star Schema Data Model, Advanced DAX, Theme JSON)
- **Documentation & Standards:** GitHub Flavored Markdown, KaTeX LaTeX Mathematical Modeling

---

## Repository Structure

```
├── data/
│   ├── raw/                           # Original telemetry data and simulation artifacts
│   │   ├── daikibo-telemetry-data.json
│   │   ├── daikibo-telemetry-data.zip
│   │   └── Dashboard_most_down_time.png
│   ├── processed/                     # Cleaned, standardized tabular data & incident logs
│   │   ├── daikibo_telemetry_clean.csv (160,704 records)
│   │   ├── downtime_incidents.csv      (29 discrete failure episodes)
│   │   ├── factory_daily_summary.csv   (124 factory-day summaries)
│   │   └── machine_health_summary.csv  (36 equipment reliability summaries)
│   └── powerbi/                       # Production star schema tables ready for Power BI
│       ├── dim_factory.csv
│       ├── dim_machine.csv
│       ├── dim_machine_type.csv
│       ├── dim_date.csv
│       ├── fact_telemetry_summary.csv
│       ├── fact_downtime_incidents.csv
│       └── dim_financial_assumptions.csv
├── notebooks_and_scripts/
│   ├── 01_data_cleaning.py            # Extraction, validation, incident grouping
│   ├── 02_eda_analysis.py             # Visual exploratory analysis & trend detection
│   ├── 03_sql_analysis.py             # SQLite setup, query execution, benchmarking
│   ├── 04_financial_impact.py         # Cost quantification & scenario modeling
│   ├── 05_predictive_maintenance.py   # ML pipeline, feature engineering, evaluation
│   └── 06_powerbi_data_prep.py        # Dimensional star schema generator
├── sql/
│   ├── daikibo_analytics.db           # Executable SQLite analytics database
│   ├── 01_factory_downtime_ranking.sql
│   ├── 02_machine_type_failures.sql
│   ├── 03_status_audit.sql
│   ├── 04_equipment_health_matrix.sql
│   ├── 05_shift_analysis.sql
│   └── 06_comprehensive_sql_suite.sql # Master consulting SQL script
├── reports/
│   ├── figures/                       # Publication-grade consulting visuals (300 DPI)
│   │   ├── 01_factory_downtime_distribution.png
│   │   ├── 02_machine_type_downtime_breakdown.png
│   │   ├── 03_factory_machine_heatmap.png
│   │   ├── 04_daily_downtime_timeline.png
│   │   ├── 06_financial_impact_by_factory.png
│   │   ├── 07_cost_breakdown_by_machine.png
│   │   ├── 08_predictive_model_roc_pr_curve.png
│   │   ├── 09_confusion_matrix_feature_importance.png
│   │   └── 10_powerbi_dashboard_preview.png
│   └── tables/                        # Exported statistical summaries
│       ├── factory_performance_kpis.csv
│       ├── machine_failure_metrics.csv
│       ├── financial_loss_summary.csv
│       ├── cost_saving_scenarios.csv
│       └── predictive_model_results.csv
├── docs/
│   ├── POWER_BI_IMPLEMENTATION_GUIDE.md  # Complete 4-page build manual
│   ├── DAX_MEASURES_DICTIONARY.md        # Full DAX formulas dictionary
│   ├── FINANCIAL_IMPACT_MODEL_SPECS.md   # Mathematical cost modeling assumptions
│   ├── PREDICTIVE_MODELING_REPORT.md     # ML architecture, curves & limitations
│   └── Daikibo_PowerBI_Theme.json        # Dark Navy & Teal Power BI theme
├── requirements.txt
├── run_pipeline.py                    # Master one-click end-to-end execution script
└── README.md
```

---

## 1. Data Cleaning & Engineering Methodology

The raw telemetry data originates from IoT sensor gateways publishing machine status packets every 10 minutes across 36 discrete machines in 4 manufacturing facilities.

### Key Data Audit Findings:
- **Total Ingested Records:** 160,704 sensor cycles.
- **Null / Missing Value Audit:** 0 missing values across all dimensions.
- **Duplicate Records Audit:** The raw JSON contains 124 contiguous blocks of 1,296 records representing 31 daily simulation iterations per factory.
- **Sensor Range:** Operational temperatures range from 23°C to 27°C (mean: 24.99°C, std: 1.41°C).
- **Failure Label Rate:** 103 unhealthy events out of 160,704 records (**0.0641% positive class prevalence**).

### Incident Episode Consolidation Logic:
In real factory operations, a machine does not experience 48 separate failures if it stays offline for 8 hours; rather, it suffers **one sustained failure incident**.
Our cleaning script groups contiguous 10-minute unhealthy intervals per machine into distinct failure episodes, categorizing them into:
- **Catastrophic Outage (> 4 hrs):** 1 incident (Seiko LaserWelder: 480 min).
- **Major Breakdown (1 - 4 hrs):** 1 incident (Meiyo HeavyDutyDrill: 70 min).
- **Minor Interruption (< 1 hr):** 27 incidents (Shenzhen LaserCutter, Meiyo LaserCutter, Berlin Furnace).

---

## 2. Exploratory Data Analysis & Strategic Insights

### Factory Downtime & Availability Ranking

| Factory Location | Country | Monitored Assets | Total Downtime (Mins) | Downtime (Hours) | Operating Availability (%) | Failure Incidents | Share of Global Downtime (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Factory Seiko (Osaka)** | Japan | 9 | 480 min | 8.00 hrs | 99.8805% | 1 | **46.60%** |
| **Shenzhen Plant** | China | 9 | 420 min | 7.00 hrs | 99.8955% | 24 | **40.78%** |
| **Factory Meiyo (Tokyo)** | Japan | 9 | 110 min | 1.83 hrs | 99.9726% | 3 | **10.68%** |
| **Berlin Facility** | Germany | 9 | 20 min | 0.33 hrs | 99.9950% | 1 | **1.94%** |
| **Global Enterprise Total** | - | **36** | **1,030 min** | **17.17 hrs** | **99.9359%** | **29** | **100.00%** |

![Factory Downtime Distribution](reports/figures/01_factory_downtime_distribution.png)

### Equipment Downtime & Reliability Breakdown

| Machine Type | Equipment Category | Total Downtime (Mins) | Downtime (Hours) | Incident Count | Share of Total Outage (%) | Mean Time To Repair (MTTR) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **LaserWelder** | Automated Fusion Joining | 480 min | 8.00 hrs | 1 | **46.60%** | 480.0 min |
| **LaserCutter** | Thermal Precision Cutting | 430 min | 7.17 hrs | 23 | **41.75%** | 18.7 min |
| **HeavyDutyDrill** | Mechanical Material Removal | 70 min | 1.17 hrs | 1 | **6.80%** | 70.0 min |
| **Furnace** | Thermal Continuous Process | 20 min | 0.33 hrs | 1 | **1.94%** | 20.0 min |
| **CNC Milling** | Precision Machining | 10 min | 0.17 hrs | 1 | **0.97%** | 10.0 min |
| **ConveyorBelt** | Material Transport Flow | 10 min | 0.17 hrs | 1 | **0.97%** | 10.0 min |
| **SpotWelder** | Subassembly Welding | 10 min | 0.17 hrs | 1 | **0.97%** | 10.0 min |
| **AirWrench** | Manual Workstation | 0 min | 0.00 hrs | 0 | 0.00% | 0.0 min (100% Uptime) |
| **MetalPress** | Stamping & Forming | 0 min | 0.00 hrs | 0 | 0.00% | 0.0 min (100% Uptime) |

![Machine Downtime Breakdown](reports/figures/02_machine_type_downtime_breakdown.png)

### Critical Failure Heatmap: Factory Location vs Equipment Type

```
                      AirWrench   CNC   Conveyor  Furnace  Drill  LaserCutter  LaserWelder  Press  SpotWelder
Berlin Facility (DE)      0        0       0        20       0         0            0         0        0
Factory Meiyo (TYO)       0        0       0         0      70        40            0         0        0
Factory Seiko (OSA)       0        0       0         0       0         0          480         0        0
Shenzhen Plant (SZX)      0       10      10         0       0       390            0         0       10
```

![Downtime Heatmap](reports/figures/03_factory_machine_heatmap.png)

### Shift Performance Analysis: The Morning Disparity
- **Shift 1 (Morning: 06:00 - 14:00):** **600 minutes of downtime (58.25% of total)**.
- **Shift 3 (Night: 22:00 - 06:00):** **290 minutes of downtime (28.16% of total)**.
- **Shift 2 (Afternoon: 14:00 - 22:00):** **140 minutes of downtime (13.59% of total)**.
*Diagnostic Finding:* The morning shift carries over 4x the downtime of the afternoon shift, driven by thermal startup drift and uninspected shift handovers.

![Daily Downtime Timeline](reports/figures/04_daily_downtime_timeline.png)

---

## 3. SQL Analytics Suite

All analytical queries were engineered and validated directly in SQLite (`sql/daikibo_analytics.db`).

### Sample Production Query: Factory Performance & Availability Scorecard
```sql
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
```

---

## 4. Financial Impact Analysis & Cost Quantification

The financial model computes three verified cost dimensions per breakdown episode:
$$\text{Total Loss} = \text{Lost Production Throughput} + \text{Emergency Technician Overtime} + \text{WIP Scrap Loss}$$

### Factory Financial Exposure Breakdown

| Factory Location | Country | Total Outage (Hrs) | Lost Production ($) | Maintenance Labor ($) | Scrap & Spoilage ($) | Total Financial Loss ($) | Share of Global Loss (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Shenzhen Plant** | China | 7.01 hrs | $6,591.50 | $1,641.60 | $5,750.00 | **$13,983.10** | **46.93%** |
| **Factory Seiko** | Japan | 8.00 hrs | $10,000.00 | $1,920.00 | $450.00 | **$12,370.00** | **41.52%** |
| **Factory Meiyo** | Japan | 1.84 hrs | $1,397.00 | $301.20 | $700.00 | **$2,398.20** | **8.05%** |
| **Berlin Facility** | Germany | 0.33 hrs | $462.00 | $79.20 | $500.00 | **$1,041.20** | **3.50%** |
| **Total Global Fleet** | - | **17.17 hrs** | **$18,450.50** | **$3,942.00** | **$7,400.00** | **$29,792.50** | **100.00%** |

![Financial Impact by Factory](reports/figures/06_financial_impact_by_factory.png)
![Cost Breakdown by Machine](reports/figures/07_cost_breakdown_by_machine.png)

### Annualized Strategic Scenarios

| Scenario Profile | Strategic Mechanism | Monthly Loss ($) | Monthly Savings ($) | Annual Net Savings ($) | Downtime Cut | Year-1 ROI ($50k Capex) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline** | Reactive "Run-to-Failure" Status Quo | $29,792.50 | $0.00 | $0.00 | 0.0% | 0.0% |
| **Scenario A** | Predictive Telemetry & Early Warning Alerts | $14,579.60 | $15,212.90 | **$182,554.80** | **60.0%** | **265.1%** |
| **Scenario B** | Rapid Response & Fast-Swap Spares Depot | $22,349.33 | $7,443.18 | **$89,318.10** | **35.0%** | **78.6%** |
| **Scenario C** | Comprehensive Industry 4.0 Transformation | $9,173.63 | $20,618.88 | **$247,426.50** | **75.0%** | **394.9%** |

---

## 5. Machine Learning Predictive Maintenance Modeling

To move from post-mortem downtime reporting to proactive condition-based intervention, three machine learning classifiers were developed to predict equipment breakdown risk (`is_unhealthy = 1`).

### Benchmark Comparison

| Model Architecture | ROC-AUC | PR-AUC (Avg Precision) | Precision | Recall (Detection Rate) | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Balanced Logistic Regression** | 0.9318 | 0.0133 | 0.43% | **85.71%** | 0.0086 |
| **Balanced Random Forest** | **0.9628** | **0.5204** | 6.85% | **71.43%** | 0.1250 |
| **Gradient Boosting Classifier** | **0.9699** | **0.4344** | **61.11%** | 52.38% | **0.5641** |

![Model ROC & PR Curves](reports/figures/08_predictive_model_roc_pr_curve.png)
![Confusion Matrix & Feature Importance](reports/figures/09_confusion_matrix_feature_importance.png)

### Key Predictive Drivers:
1. `device_type_LaserCutter` (Gini: **0.284**) & `device_type_LaserWelder` (Gini: **0.192**): High mechanical/optical wear profile.
2. `factory_code_FAC-SZX-04` (Gini: **0.141**): Elevated operational temperature and usage intensity.
3. `temp_rolling_std_6` (Gini: **0.089**): Rapid thermal fluctuation preceding internal failure.

---

## 6. Microsoft Power BI Executive Dashboard Suite

A modern four-page Power BI dashboard suite was designed conforming to global consulting data visualization standards.

### 4K Master Dashboard Suite Showcase
![Master Power BI Dashboard Suite](reports/figures/powerbi_full_suite_master_showcase.png)

### Page-by-Page Visual Tour

#### Page 1: Executive Overview
*Fleetwide cockpit tracking Global Availability (99.94%), Total Downtime (17.17 hrs), Factory Outage Distribution, Equipment Contribution Donut, 31-Day Trend Timeline, and Global Geographic Plant Scorecard.*
![Page 1 Executive Overview](reports/figures/powerbi_page_1_executive_overview.png)

#### Page 2: Factory Performance & Benchmarking
*Cross-facility reliability comparisons featuring the 58% Morning Shift Disparity column chart, Shop-Floor Section Heatmap (Shenzhen Section 3 vulnerability), and the Master Operations Scorecard Matrix.*
![Page 2 Factory Performance](reports/figures/powerbi_page_2_factory_performance.png)

#### Page 3: Machine Analytics & Reliability
*Engineering diagnostics featuring the MTBF vs MTTR Reliability Scatter Matrix, Failure Incident Frequency rankings (LaserCutter: 23 incidents), Failure Severity distribution, and Granular Incident Outage Log.*
![Page 3 Machine Analytics](reports/figures/powerbi_page_3_machine_analytics.png)

#### Page 4: Financial Impact & Risk Simulator
*Cost quantification breakdown (Throughput Loss vs Labor vs Scrap), Machine-Type Treemap, Interactive What-If Parameter Slicer (75% downtime reduction selected), and Strategic Scenario Payoff Comparison ($247k/yr net savings).*
![Page 4 Financial Impact](reports/figures/powerbi_page_4_financial_risk.png)

### Summary of Dashboard Pages:
1. **PAGE 1: EXECUTIVE OVERVIEW**  
   Fleetwide cockpit tracking Global Availability (99.94%), Total Downtime (17.17 hrs), Total Incidents (29), Factory Breakdown Distribution, and Machine Downtime Donut Chart.
2. **PAGE 2: FACTORY PERFORMANCE**  
   Regional benchmarking comparing Meiyo, Seiko, Berlin, and Shenzhen. Features Factory Section heatmaps, Shift Variance column charts, and the Factory Operational Scorecard.
3. **PAGE 3: MACHINE ANALYTICS & RELIABILITY**  
   Deep asset-level diagnostics with MTBF vs MTTR Reliability Scatter Matrix, Incident Frequency rankings, Failure Severity breakdown, and Granular Maintenance Incident Log.
4. **PAGE 4: FINANCIAL IMPACT & WHAT-IF RISK MODEL**  
   Cost quantification breakdown (Lost Production, Labor, Scrap), Machine-Type Treemap, and an interactive **What-If Downtime Reduction Parameter Slicer** modeling real-time ROI and dollar savings.

> Complete build instructions and visual settings are provided in [docs/POWER_BI_IMPLEMENTATION_GUIDE.md](docs/POWER_BI_IMPLEMENTATION_GUIDE.md).  
> All 20+ DAX formulas are documented in [docs/DAX_MEASURES_DICTIONARY.md](docs/DAX_MEASURES_DICTIONARY.md).  
> Custom Dark Navy theme is available in [docs/Daikibo_PowerBI_Theme.json](docs/Daikibo_PowerBI_Theme.json).

---

## 7. Strategic Business Recommendations

Based on empirical analytical findings, we present five actionable, prioritized strategic recommendations for Daikibo Industrials' executive committee:

### 1. Eliminate Catastrophic Outages at Factory Seiko via Condition Monitoring
- **Analytical Finding:** Factory Seiko lost **480 minutes (8.0 hours)** in a single catastrophic shift outage on its LaserWelder ($12,370 loss).
- **Action:** Install high-frequency thermal and vibration IoT sensors on the LaserWelder diode cavity and cooling lines with automated threshold alarms dispatching technicians before thermal shutdown occurs.
- **Financial Payoff:** Protects **$10,000+ in lost throughput per breakdown event**.

### 2. Overhaul LaserCutter Preventive Maintenance at Shenzhen Plant
- **Analytical Finding:** Shenzhen Plant suffered **21 distinct LaserCutter breakdown incidents** across 14 operational days, generating **$5,750 in scrap and ruined workpieces**.
- **Action:** Shift from 30-day scheduled maintenance to a dynamic 48-hour optical lens cleaning and nozzle alignment inspection checklist; replace worn gas delivery nozzles proactively.
- **Financial Payoff:** Recaptures **$5,750 in monthly scrap losses** ($69,000/year).

### 3. Mitigate Morning Shift Startup Failure Spike (The 58% Rule)
- **Analytical Finding:** Morning Shift (06:00 - 14:00) accounts for **58.25% of all global downtime (600 minutes)**.
- **Action:** Implement a standardized 15-minute machine warm-up and dry-cycle calibration routine prior to full-speed morning production ramp-up; audit shift handover logs.
- **Financial Payoff:** Reduces fleetwide downtime by an estimated **30-40%**, capturing ~$7,000 monthly savings.

### 4. Codify the "Berlin Operational Standard" as Global Center of Excellence
- **Analytical Finding:** Berlin Facility achieved **99.995% operational availability** (only 20 min downtime, 0 min across 8 of 9 machines).
- **Action:** Conduct an operational audit of Berlin's preventative maintenance scheduling, technician training protocols, and lubrication regimes to serve as Daikibo's global manufacturing operating blueprint.
- **Financial Payoff:** Lifts underperforming plants toward the 99.99% availability frontier.

### 5. Execute Industry 4.0 Predictive Maintenance Transformation (Scenario C)
- **Analytical Finding:** Transitioning from reactive maintenance to integrated predictive telemetry and standardized fast-swap spares cuts downtime by 75% and scrap by 65%.
- **Action:** Deploy the Random Forest predictive model on local edge gateways, paired with a localized critical spare parts inventory for laser components.
- **Financial Payoff:** Delivers **$247,426.50 in net annualized operational savings** with a Year-1 ROI of **394.9%** and a **2.4-month capital payback**.

---

## 8. Installation & Execution Guide

### Prerequisites
- Python 3.10+ installed.
- Microsoft Power BI Desktop (for opening and building the dashboard).

### Setup & Pipeline Execution
```bash
# 1. Clone the repository
git clone https://github.com/your-username/Manufacturing-Operations-Predictive-Maintenance.git
cd Manufacturing-Operations-Predictive-Maintenance

# 2. Install required Python packages
pip install -r requirements.txt

# 3. Run the complete automated data pipeline end-to-end
python run_pipeline.py
```

### Building the Power BI Dashboard
1. Open **Microsoft Power BI Desktop**.
2. Go to **View > Themes > Browse for themes** and select `docs/Daikibo_PowerBI_Theme.json`.
3. Import the clean CSV tables located in `data/powerbi/`.
4. Create the relationships shown in `docs/DAX_MEASURES_DICTIONARY.md`.
5. Follow the visual-by-visual layout instructions in `docs/POWER_BI_IMPLEMENTATION_GUIDE.md`.

---

## License & Attribution
- **Dataset Attribution:** Daikibo Factory Telemetry dataset provided via the [Deloitte Australia Data Analytics Job Simulation](https://www.theforage.com/) hosted on Forage.
- **Project License:** MIT License. Developed for portfolio, enterprise analytics, and management consulting demonstration.

