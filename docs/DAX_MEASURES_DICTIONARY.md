# DAX Measures Dictionary & Data Modeling Guide
**Project:** Manufacturing Operations & Predictive Maintenance Analytics  
**Client Simulation:** Daikibo Industrials (Deloitte Australia Data Analytics Job Simulation)  
**Author:** Senior Data Analyst & Business Intelligence Consultant  

---

## 1. Data Model Architecture (Star Schema)

The Power BI data model is structured as a high-performance **Star Schema** with one-to-many (`1:*`) directional filtering from dimensions to fact tables:

```
                  ┌──────────────────────┐
                  │      dim_date        │
                  │  (Date, Day, Week)   │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ * (calendar_date)
┌──────────────────┐  1      ▼      *   ┌──────────────────────┐
│   dim_factory    ├───────────────────┤fact_telemetry_summary│
│(Code, Name, Geo) │◄──┐            ┌──┤ (Cycles, Mins, Temp) │
└──────────────────┘   │            │   └──────────────────────┘
                       │ 1          │ 1
                       │            │
┌──────────────────┐   │ *          │ * ┌──────────────────────┐
│   dim_machine    ├───┼────────────┴──┤fact_downtime_incidents│
│(DeviceID, Type)  │   └───────────────┤ (Loss, Severity, Cat)│
└────────┬─────────┘ 1                  └───────────┬──────────┘
         │                                          │ *
         │ *                                        │
┌────────┴─────────┐ 1                              │ 1
│ dim_machine_type │                                │
│ (Type, Critical) │                                │
└──────────────────┘                  ┌─────────────┴──────────┐
                                      │dim_financial_assumptions│
                                      │ (Hourly Rates, Scrap)  │
                                      └────────────────────────┘
```

### Table Relationships & Cardinality:
1. `dim_factory[factory_code]` (1) ───> `fact_telemetry_summary[factory_code]` (*)
2. `dim_factory[factory_code]` (1) ───> `fact_downtime_incidents[factory_code]` (*)
3. `dim_machine[device_id]` (1) ───> `fact_telemetry_summary[device_id]` (*)
4. `dim_machine[device_id]` (1) ───> `fact_downtime_incidents[device_id]` (*)
5. `dim_machine_type[device_type]` (1) ───> `dim_machine[device_type]` (*)
6. `dim_date[date]` (1) ───> `fact_telemetry_summary[calendar_date]` (*)
7. `dim_date[date]` (1) ───> `fact_downtime_incidents[calendar_date]` (*)

---

## 2. Core Volume & Operational DAX Measures

### `[Total Factories]`
```dax
Total Factories = 
DISTINCTCOUNT(dim_factory[factory_code])
```
*Description:* Returns the total number of manufacturing facilities in the global network (4 plants: Meiyo, Seiko, Berlin, Shenzhen).

### `[Total Machines]`
```dax
Total Machines = 
DISTINCTCOUNT(dim_machine[device_id])
```
*Description:* Counts the total active monitored machine assets across all factories (36 devices).

### `[Total Telemetry Records]`
```dax
Total Telemetry Records = 
SUM(fact_telemetry_summary[total_cycles])
```
*Description:* Computes the total number of 10-minute sensor telemetry cycles ingested (160,704 cycles).

### `[Healthy Telemetry Events]`
```dax
Healthy Telemetry Events = 
SUM(fact_telemetry_summary[healthy_cycles])
```
*Description:* Sum of all normal operating intervals where equipment status was logged as "Healthy" (160,601 cycles).

### `[Unhealthy Telemetry Events]`
```dax
Unhealthy Telemetry Events = 
SUM(fact_telemetry_summary[unhealthy_cycles])
```
*Description:* Sum of all breakdown intervals where equipment status was logged as "Unhealthy" (103 cycles).

---

## 3. Equipment Downtime & Availability DAX Measures

### `[Total Downtime Minutes]`
```dax
Total Downtime Minutes = 
SUM(fact_telemetry_summary[downtime_minutes])
```
*Description:* Total duration of equipment outage across the system in minutes (1,030 minutes).

### `[Total Downtime Hours]`
```dax
Total Downtime Hours = 
DIVIDE([Total Downtime Minutes], 60, 0)
```
*Description:* Total downtime converted to decimal hours (17.17 hours).

### `[Planned Operating Hours]`
```dax
Planned Operating Hours = 
DIVIDE([Total Telemetry Records] * 10, 60, 0)
```
*Description:* Total scheduled production availability based on 24/7 continuous operation across 36 machines over 31 days (26,784 operating hours).

### `[Operational Availability %]`
```dax
Operational Availability % = 
VAR PlannedHours = [Planned Operating Hours]
VAR DowntimeHours = [Total Downtime Hours]
RETURN
DIVIDE(PlannedHours - DowntimeHours, PlannedHours, 1.0) * 100
```
*Description:* Primary plant availability metric. Global baseline sits at **99.9359%**.

### `[Downtime Share %]`
```dax
Downtime Share % = 
DIVIDE(
    [Total Downtime Minutes],
    CALCULATE([Total Downtime Minutes], ALL(dim_factory), ALL(dim_machine)),
    0
) * 100
```
*Description:* Computes the percentage contribution of a selected factory or machine type to total global downtime.

---

## 4. Maintenance Engineering KPIs (MTBF, MTTR, Health Score)

### `[Total Failure Incidents]`
```dax
Total Failure Incidents = 
COUNTROWS(fact_downtime_incidents)
```
*Description:* Total discrete breakdown episodes where equipment required intervention (29 incidents).

### `[MTBF Hours (Mean Time Between Failures)]`
```dax
MTBF Hours = 
VAR OperatingHours = [Planned Operating Hours] - [Total Downtime Hours]
VAR Incidents = [Total Failure Incidents]
RETURN
IF(
    Incidents > 0,
    DIVIDE(OperatingHours, Incidents, OperatingHours),
    OperatingHours
)
```
*Description:* Reliability metric indicating the average operating hours between consecutive equipment failures.

### `[MTTR Minutes (Mean Time To Repair)]`
```dax
MTTR Minutes = 
DIVIDE([Total Downtime Minutes], [Total Failure Incidents], 0)
```
*Description:* Maintainability metric indicating the average elapsed time required to diagnose, repair, and restore equipment to operational state. Global average is **35.52 minutes per incident** (ranging from 10 min micro-stops to 480 min catastrophic breakdown).

### `[Equipment Health Score]`
```dax
Equipment Health Score = 
VAR Avail = [Operational Availability %]
VAR IncidentPenalty = [Total Failure Incidents] * 0.25
VAR Score = Avail - IncidentPenalty
RETURN
MAX(0, MIN(100, Score))
```
*Description:* Composite health score index (0 to 100%) reflecting operational uptime adjusted for breakdown frequency.

---

## 5. Financial Impact & Cost Quantification DAX Measures

### `[Total Financial Loss]`
```dax
Total Financial Loss = 
SUM(fact_downtime_incidents[total_financial_loss])
```
*Description:* Combined financial loss resulting from machine breakdown, comprising lost throughput, emergency technician labor, and scrap spoilage ($29,792.50).

### `[Lost Production Cost]`
```dax
Lost Production Cost = 
SUM(fact_downtime_incidents[lost_production_cost])
```
*Description:* Value of unproduced goods and starved assembly lines during downtime ($18,450.50).

### `[Maintenance Labor Cost]`
```dax
Maintenance Labor Cost = 
SUM(fact_downtime_incidents[maintenance_labor_cost])
```
*Description:* Direct technician repair wages during emergency breakdown recovery ($3,942.00).

### `[Scrap & Spoilage Cost]`
```dax
Scrap & Spoilage Cost = 
SUM(fact_downtime_incidents[scrap_spoilage_cost])
```
*Description:* Direct cost of ruined work-in-progress (WIP) materials and defective parts scrapped upon machine stoppage ($7,400.00).

### `[Annualized Financial Loss]`
```dax
Annualized Financial Loss = 
[Total Financial Loss] * 12
```
*Description:* 12-month projection of operational losses assuming baseline maintenance practices continue ($357,510.00 / year).

### `[Financial Loss per Downtime Hour]`
```dax
Financial Loss per Downtime Hour = 
DIVIDE([Total Financial Loss], [Total Downtime Hours], 0)
```
*Description:* Average financial burn rate per hour of equipment downtime across the fleet ($1,735.15 / hour).

---

## 6. What-If Predictive Scenario Modeling DAX

### `[Simulated Downtime Reduction %]`
```dax
Simulated Downtime Reduction % = 
SELECTEDVALUE('Scenario Parameter'[Parameter Value], 0.60)
```
*Description:* Dynamic parameter driven by a Power BI What-If Slicer (slider from 0% to 100%).

### `[Projected Monthly Savings ($)]`
```dax
Projected Monthly Savings = 
[Total Financial Loss] * [Simulated Downtime Reduction %]
```
*Description:* Real-time modeled monthly savings achieved through early warning condition-monitoring.

### `[Projected Annual Savings ($)]`
```dax
Projected Annual Savings = 
[Projected Monthly Savings] * 12
```
*Description:* Annualized financial savings delivered by the predictive maintenance initiative.

### `[Predictive Maintenance Program ROI %]`
```dax
Predictive Maintenance Program ROI % = 
VAR ImplementationCost = 50000 -- Estimated IoT sensor gateway & ML software license ($50k)
VAR AnnualBenefit = [Projected Annual Savings]
RETURN
DIVIDE(AnnualBenefit - ImplementationCost, ImplementationCost, 0) * 100
```
*Description:* Return on Investment (ROI) for executive decision-making. At 60% downtime reduction, Year 1 ROI reaches **265.1%**.

