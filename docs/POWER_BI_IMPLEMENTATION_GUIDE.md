# Power BI Desktop Implementation Guide
## Manufacturing Operations & Predictive Maintenance Analytics
**Client Simulation:** Daikibo Industrials  
**Technology:** Microsoft Power BI Desktop  
**Design Standard:** Dark Navy Consulting Enterprise Suite (Deloitte / PwC / KPMG Benchmark)  
**Theme Colors:** Dark Navy (`#0B132B`), Card Canvas (`#1C2541`), Cyan Accent (`#00F2FE`), Electric Blue (`#4FACFE`), Emerald (`#10B981`), Amber (`#F59E0B`), Coral (`#F43F5E`)  

---

## 1. Quick Start & Data Import

1. **Launch Microsoft Power BI Desktop**.
2. **Apply Theme**:
   - Go to **View** > **Themes** dropdown > **Browse for themes**.
   - Select `docs/Daikibo_PowerBI_Theme.json` from this project repository.
3. **Import Data Sources** (Text/CSV):
   - Navigate to `data/powerbi/` folder.
   - Import the following CSV files:
     1. `dim_factory.csv`
     2. `dim_machine.csv`
     3. `dim_machine_type.csv`
     4. `dim_date.csv`
     5. `fact_telemetry_summary.csv`
     6. `fact_downtime_incidents.csv`
     7. `dim_financial_assumptions.csv`
4. **Verify Data Types**:
   - `dim_date[date]`: Date
   - `fact_telemetry_summary[calendar_date]`: Date
   - `fact_downtime_incidents[calendar_date]`: Date
   - `dim_factory[latitude]` & `[longitude]`: Decimal number (Data Category: Latitude / Longitude)
   - Numerical metrics (`downtime_minutes`, `total_financial_loss`, etc.): Whole Number / Decimal Number.

---

## 2. Model View & Relationship Configuration

Switch to **Model View** in Power BI Desktop and confirm the following 1-to-many (`1:*`) relationships with **Single** cross-filter direction:

| From Table (Dimension - 1) | Key Column | To Table (Fact - *) | Foreign Key Column | Cardinality | Cross Filter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`dim_factory`** | `factory_code` | **`fact_telemetry_summary`** | `factory_code` | 1 to Many (`1:*`) | Single |
| **`dim_factory`** | `factory_code` | **`fact_downtime_incidents`** | `factory_code` | 1 to Many (`1:*`) | Single |
| **`dim_machine`** | `device_id` | **`fact_telemetry_summary`** | `device_id` | 1 to Many (`1:*`) | Single |
| **`dim_machine`** | `device_id` | **`fact_downtime_incidents`** | `device_id` | 1 to Many (`1:*`) | Single |
| **`dim_machine_type`** | `device_type` | **`dim_machine`** | `device_type` | 1 to Many (`1:*`) | Single |
| **`dim_date`** | `date` | **`fact_telemetry_summary`** | `calendar_date` | 1 to Many (`1:*`) | Single |
| **`dim_date`** | `date` | **`fact_downtime_incidents`** | `calendar_date` | 1 to Many (`1:*`) | Single |

---

## 3. Creating DAX Measures

Create a dedicated blank table named `_Measures` (**Home** > **Enter Data** > Name: `_Measures`).  
Right-click `_Measures` and add the DAX measures detailed in `docs/DAX_MEASURES_DICTIONARY.md`.

Key measures required for dashboard visual cards:
- `[Total Factories]`
- `[Total Machines]`
- `[Total Telemetry Records]`
- `[Unhealthy Telemetry Events]`
- `[Total Downtime Hours]`
- `[Operational Availability %]`
- `[Total Failure Incidents]`
- `[MTBF Hours]`
- `[MTTR Minutes]`
- `[Total Financial Loss]`
- `[Lost Production Cost]`
- `[Maintenance Labor Cost]`
- `[Scrap & Spoilage Cost]`
- `[Simulated Annual Savings]`

---

## 4. Canvas Formatting & Global Header Template

For all four dashboard pages, set the canvas background:
- **Canvas Settings**: Type: Custom (16:9 widescreen, `1280 x 720` or `1920 x 1080`).
- **Canvas Background**: Color: `#0B132B`, Transparency: `0%`.
- **Top Header Bar**:
  - Insert a Rectangle Shape across the top (`Y=0, Height=60`).
  - Fill: `#1C2541`, Border: None.
  - Add Text Box: **"DAIKIBO INDUSTRIALS | Manufacturing Operations & Predictive Maintenance"** (`Segoe UI Semibold, 16pt, #F8FAFC`).
  - Add Subtitle: *"Enterprise Telemetry Analytics & Equipment Reliability Suite"* (`Segoe UI, 10pt, #94A3B8`).
  - Add Slicers in Header (Right Side):
    - **Factory Slicer**: `dim_factory[factory_name]` (Dropdown style).
    - **Date Range Slicer**: `dim_date[date]` (Between style).
    - **Shift Slicer**: `fact_telemetry_summary[shift]` (Horizontal buttons / Tile style).

---

## 5. Detailed Page Construction Guide

---

### PAGE 1: EXECUTIVE OVERVIEW
**Purpose:** High-level executive cockpit summarizing system health, production availability, critical downtime, and global asset distribution.

#### A. Top KPI Cards Row (Cards / New Card Visual, Y=70, Height=90)
1. **Card 1: Global Facilities**
   - Field: `[Total Factories]`
   - Display: **4 Factories**
   - Accent: Teal (`#00F2FE`)
2. **Card 2: Monitored Machines**
   - Field: `[Total Machines]`
   - Display: **36 Assets**
   - Accent: Cyan (`#4FACFE`)
3. **Card 3: Telemetry Readings**
   - Field: `[Total Telemetry Records]`
   - Display: **160,704 Cycles**
   - Accent: Blue (`#38BDF8`)
4. **Card 4: Total Downtime**
   - Field: `[Total Downtime Hours]`
   - Sub-label: `[Total Downtime Minutes]` & "1,030 mins"
   - Display: **17.17 Hrs**
   - Accent: Coral (`#F43F5E`)
5. **Card 5: Operational Availability**
   - Field: `[Operational Availability %]`
   - Display: **99.94%** (Target: >99.85%)
   - Accent: Emerald (`#10B981`)
6. **Card 6: Breakdown Incidents**
   - Field: `[Total Failure Incidents]`
   - Display: **29 Events**
   - Accent: Amber (`#F59E0B`)

#### B. Main Visuals Grid (Y=175)
- **Visual 1 (Top Left, 50% width): Clustered Bar Chart - Downtime by Factory**
  - **Y-Axis**: `dim_factory[factory_name]`
  - **X-Axis**: `[Total Downtime Minutes]`
  - **Data Color**: Conditional formatting (Seiko: `#F43F5E`, Shenzhen: `#F59E0B`, Meiyo: `#00F2FE`, Berlin: `#10B981`).
  - **Data Labels**: Enabled (Show value in minutes and hours).
- **Visual 2 (Top Right, 50% width): Donut Chart - Equipment Downtime Contribution by Machine Type**
  - **Legend**: `dim_machine_type[device_type]`
  - **Values**: `[Total Downtime Minutes]`
  - **Detail Labels**: Category + Percent of Total.
  - Highlights: LaserWelder (46.6%) and LaserCutter (41.7%) consume 88.3% of all downtime.
- **Visual 3 (Bottom Left, 60% width): Line & Clustered Column Chart - Daily Downtime & Health Trajectory**
  - **Shared X-Axis**: `dim_date[day_of_month]` (Days 1 to 31)
  - **Column Values**: `[Total Downtime Minutes]`
  - **Line Values**: `[Operational Availability %]` (Secondary Y-Axis: Scale 98% to 100%)
  - Highlights: Clear visual spike on Day 15 (480 min outage).
- **Visual 4 (Bottom Right, 40% width): Filled Map / Bubble Map - Global Facility Status**
  - **Latitude**: `dim_factory[latitude]`
  - **Longitude**: `dim_factory[longitude]`
  - **Size**: `[Total Downtime Minutes]`
  - **Color / Legend**: `dim_factory[country]`
  - Tooltips: Factory Name, Operating Availability %, Total Incidents, Plant Workforce.

---

### PAGE 2: FACTORY PERFORMANCE
**Purpose:** Regional benchmark comparison across the four production plants to identify operational disparities, shift-level variance, and factory-specific failure patterns.

#### A. KPI Cards Header
- `[Factory Availability %]`, `[Factory Downtime Hours]`, `[Incident Frequency]`, `[Plant Workforce]`.

#### B. Visuals Grid
- **Visual 1 (Top Left): Stacked Bar Chart - Equipment Downtime Distribution by Factory Section**
  - **Y-Axis**: `dim_factory[factory_name]`
  - **X-Axis**: `[Total Downtime Minutes]`
  - **Legend**: `dim_machine[section]` (Section 1, 2, 3, 4)
  - Insight: Section 3 in Shenzhen and Section 4 in Seiko represent concentrated risk zones.
- **Visual 2 (Top Right): Grouped Column Chart - Operational Downtime by Shift**
  - **X-Axis**: `fact_telemetry_summary[shift]` (Morning, Afternoon, Night)
  - **Y-Axis**: `[Total Downtime Minutes]`
  - **Legend**: `dim_factory[factory_name]`
  - Insight: Morning Shift accounts for 58.25% of all global downtime.
- **Visual 3 (Bottom Left): Matrix Table - Factory Operations Scorecard**
  - **Rows**: `dim_factory[factory_name]`
  - **Values**:
    - `[Total Machines]`
    - `[Total Telemetry Records]`
    - `[Unhealthy Telemetry Events]`
    - `[Total Downtime Minutes]`
    - `[Operational Availability %]`
    - `[Total Failure Incidents]`
    - `[MTBF Hours]`
    - `[MTTR Minutes]`
  - **Conditional Formatting**: Background color scale on `[Operational Availability %]` (Green to Red).
- **Visual 4 (Bottom Right): Ribbon / Area Chart - Daily Factory Downtime Comparison**
  - **X-Axis**: `dim_date[day_of_month]`
  - **Y-Axis**: `[Total Downtime Minutes]`
  - **Legend**: `dim_factory[factory_name]`

---

### PAGE 3: MACHINE ANALYTICS & RELIABILITY
**Purpose:** Granular diagnostics into machine health, failure mechanics (catastrophic vs chronic intermittent micro-stops), MTBF, and MTTR.

#### A. KPI Cards
- `[Avg MTBF Hours]` (923.6 hrs), `[Avg MTTR Minutes]` (35.5 mins), `[Fleet Health Index]` (99.2%), `[Chronic Failure Assets]` (1 asset).

#### B. Visuals Grid
- **Visual 1 (Top Left): Scatter Plot - Reliability Matrix (MTBF vs MTTR)**
  - **X-Axis**: `[MTTR Minutes]` (Log or Linear scale)
  - **Y-Axis**: `[MTBF Hours]`
  - **Details**: `dim_machine[device_type]` or `dim_machine[device_id]`
  - **Size**: `[Total Downtime Minutes]`
  - **Color**: `dim_factory[factory_name]`
  - **Quadrant Annotation**: Top-Left = Highly Reliable (High MTBF, Low MTTR); Bottom-Right = Critical Bottleneck (Low MTBF, High MTTR).
- **Visual 2 (Top Right): Horizontal Bar Chart - Failure Frequency (Incident Counts) by Machine**
  - **Y-Axis**: `dim_machine_type[device_type]`
  - **X-Axis**: `[Total Failure Incidents]`
  - **Data Color**: `#4FACFE`
  - Insight: LaserCutter accounts for 23 of 29 incidents (79.3% of all breakdowns).
- **Visual 3 (Bottom Left): Stacked Bar Chart - Failure Severity Classification**
  - **Y-Axis**: `dim_machine_type[device_type]`
  - **X-Axis**: `[Total Downtime Minutes]`
  - **Legend**: `fact_downtime_incidents[severity_classification]`
  - Categories: Catastrophic (>4 hrs), Major Breakdown (1-4 hrs), Minor Interruption (<1 hr).
- **Visual 4 (Bottom Right): Table - Critical Asset Failure Log**
  - **Columns**: `incident_id`, `factory_name`, `device_type`, `section`, `calendar_date`, `shift`, `duration_minutes`, `avg_temperature_c`, `severity_classification`.

---

### PAGE 4: FINANCIAL IMPACT & WHAT-IF RISK MODEL
**Purpose:** Monetization of equipment downtime, financial loss attribution by cost component, and interactive scenario simulation for executive investment justification.

#### A. KPI Cards
- `[Total Financial Loss]` (**$29,792.50**), `[Lost Production Cost]` (**$18,450.50**), `[Scrap & Spoilage Cost]` (**$7,400.00**), `[Annualized Exposure]` (**$357,510.00**).

#### B. Visuals Grid
- **Visual 1 (Top Left): 100% Stacked Column Chart - Financial Cost Breakdown by Factory**
  - **X-Axis**: `dim_factory[factory_name]`
  - **Y-Axis**: Cost Components (`[Lost Production Cost]`, `[Maintenance Labor Cost]`, `[Scrap & Spoilage Cost]`)
  - **Colors**: Lost Production: Coral (`#F43F5E`), Labor: Cyan (`#00F2FE`), Scrap: Amber (`#F59E0B`).
  - Insight: Shenzhen has higher scrap cost due to 24 breakdown incidents ($5,750 scrap).
- **Visual 2 (Top Right): Treemap - Financial Loss Attribution by Machine Type**
  - **Group**: `dim_machine_type[device_type]`
  - **Values**: `[Total Financial Loss]`
  - **Data Labels**: Value and Percentage of Total.
- **Visual 3 (Bottom Left): What-If Slicer & Scenario Modeling Card**
  - **What-If Parameter**: Go to **Modeling** > **New Parameter** > **Numeric Range**:
    - Name: `Downtime Reduction %`
    - Data Type: Decimal number
    - Minimum: 0.0, Maximum: 1.0, Increment: 0.05, Default: 0.60 (60%).
  - **Output Card 1**: `[Projected Monthly Savings]` ($17,875 at 60%).
  - **Output Card 2**: `[Projected Annual Savings]` ($214,500/year).
  - **Output Card 3**: `[Predictive Maintenance Program ROI %]` (**329% ROI** on a $50k investment).
- **Visual 4 (Bottom Right): Clustered Bar Chart - Strategic Scenario Comparison**
  - **Y-Axis**: Scenario Name (Baseline, Scenario A, Scenario B, Scenario C).
  - **X-Axis**: Annual Net Financial Loss ($).
  - Clearly demonstrates how Scenario C reduces annual financial exposure from **$357.5k down to $110.1k** (delivering **$247.4k in net savings**).

---

## 6. Interaction, Drill-Through & Slicers

1. **Cross-Filtering**: Ensure clicking on any factory bar in Page 1 or Page 2 filters all related machine and trend visuals automatically.
2. **Drill-Through Target**: Configure Page 3 (Machine Analytics) as a Drill-Through page:
   - In Page 3 Visualizations pane, add `dim_machine[device_type]` and `dim_factory[factory_name]` to the **Drill-through fields** well.
   - Users can right-click any factory or machine visual on Page 1 or Page 2 and select **Drill through > Machine Analytics** to see instant diagnostics.
3. **Bookmarks & Navigation**:
   - Create a clean navigation ribbon using Power BI Page Navigator buttons (**Insert** > **Buttons** > **Page Navigator**) positioned at the top left under the logo.

