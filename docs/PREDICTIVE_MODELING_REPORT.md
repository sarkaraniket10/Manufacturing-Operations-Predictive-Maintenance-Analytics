# Machine Learning Predictive Maintenance Modeling Report
**Project:** Manufacturing Operations & Predictive Maintenance Analytics  
**Client:** Daikibo Industrials Global Telemetry Analytics  
**Methodology:** Supervised Anomaly & Failure Risk Classification  
**Frameworks:** Python, Scikit-learn, Pandas, NumPy  

---

## 1. Problem Formulation & Objective

The objective of this predictive analytics module is to develop an early-warning machine health classification model capable of detecting equipment failure risk (`is_unhealthy = 1`) prior to severe downtime occurrence.

In industrial operations, detecting equipment degradation early allows maintenance teams to transition from **reactive maintenance** (costly catastrophic failures) to **condition-based predictive maintenance** (scheduled low-impact servicing during planned changeovers).

---

## 2. Dataset Characteristics & The Rare Event Challenge

The dataset contains **160,704 sensor telemetry readings** across 36 manufacturing assets.

### Class Imbalance Profile:
- **Healthy Cycles (`0`)**: 160,601 records (**99.9359%**)
- **Unhealthy Cycles (`1`)**: 103 records (**0.0641%**)
- **Imbalance Ratio**: Approximately **1 : 1,559** (extreme rare event anomaly detection problem).

> [!WARNING]  
> In extreme class imbalance scenarios, standard accuracy is misleading: a trivial model predicting 100% "Healthy" achieves **99.94% accuracy** while completely failing to detect every single breakdown. Models must be evaluated strictly using **ROC-AUC**, **Precision-Recall AUC (PR-AUC)**, **Recall (Sensitivity)**, and **F1-Score**.

---

## 3. Feature Engineering Pipeline

To capture operational dynamics and failure precursors, 24 engineered features were derived:
1. **Sensor Telemetry Dynamics**:
   - `temperature_c`: Current operational temperature.
   - `temp_rolling_mean_6`: Rolling 1-hour average temperature (6 10-minute intervals).
   - `temp_rolling_std_6`: Rolling 1-hour temperature volatility/fluctuation index.
   - `temp_diff_prev`: Instantaneous rate of temperature change relative to previous reading.
2. **Operational Stress & Elapsed Time**:
   - `operating_hours_in_batch`: Cumulative elapsed runtime hours within the daily production batch.
   - `block_step`: Telemetry cycle index within current operational block.
3. **Temporal & Shift Dynamics**:
   - `hour_sin` & `hour_cos`: Cyclical sine/cosine transformation of diurnal operational hour.
   - `shift`: Categorical encoding of Morning, Afternoon, and Night shifts.
   - `day_of_month`: Day index (1 to 31) across the operational period.
4. **Asset Categorical Hierarchy**:
   - One-hot encoded `device_type` (capturing high-risk laser assets).
   - One-hot encoded `factory_code` (capturing regional plant stress profiles).
   - One-hot encoded `section` (capturing work cell location).

---

## 4. Model Training & Benchmarking

The dataset was split using an **80/20 Stratified Train-Test Split** (128,563 training instances with 82 failures; 32,141 test instances with 21 failures).

Three distinct algorithmic paradigms were benchmarked:
1. **Balanced Logistic Regression**: Linear baseline with inverse class weight regularization.
2. **Balanced Random Forest Classifier**: Ensemble of 100 decision trees utilizing `balanced_subsample` bootstrap weighting to ensure failure events are adequately represented in every decision tree.
3. **Gradient Boosting Classifier (GBM)**: Sequential ensemble optimizing gradient boosting deviance with early stopping.

### Performance Benchmark Results:

| Model Architecture | ROC-AUC | PR-AUC (Avg Precision) | Precision | Recall (Detection Rate) | F1-Score | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Balanced Logistic Regression** | 0.9318 | 0.0133 | 0.43% | **85.71%** | 0.0086 | < 1 ms |
| **Balanced Random Forest** | **0.9628** | **0.5204** | 6.85% | **71.43%** | 0.1250 | 2.4 ms |
| **Gradient Boosting Classifier** | **0.9699** | **0.4344** | **61.11%** | 52.38% | **0.5641** | 3.1 ms |

---

## 5. Model Evaluation & Key Findings

### 1. ROC-AUC vs PR-AUC Analysis
- All models achieved high **ROC-AUC scores (>0.93)**. However, on highly imbalanced telemetry datasets, **PR-AUC** provides the true measure of discrimination.
- **Balanced Random Forest** achieved the highest PR-AUC (**0.5204**), detecting **71.43% of all machine breakdowns** (15 out of 21 test failures successfully flagged) while minimizing false alarms compared to linear regression.
- **Gradient Boosting** achieved superior Precision (**61.11%**), making it ideal when maintenance dispatch costs are high and false alarm fatigue must be prevented.

### 2. Feature Importance Analysis (Top Risk Drivers)
Analysis of Gini importance from the Random Forest model reveals the primary failure indicators:
1. `device_type_LaserCutter` (Importance: **0.284**): Single greatest failure indicator due to high failure recurrence in Shenzhen and Meiyo.
2. `device_type_LaserWelder` (Importance: **0.192**): High impact driver corresponding to catastrophic shift failure at Seiko.
3. `factory_code_FAC-SZX-04` (Shenzhen) (Importance: **0.141**): Facility environment factor.
4. `temp_rolling_std_6` (Importance: **0.089**): Rapid fluctuations in operational temperature preceding component instability.
5. `operating_hours_in_batch` (Importance: **0.076**): Equipment fatigue accumulating over continuous operating hours.
6. `hour_sin` / `hour_cos` (Importance: **0.065**): Diurnal morning-shift startup stress.

---

## 6. Critical Model Limitations & Production Deployment Roadmap

While the models demonstrate strong predictive capability, senior data analysts must transparently document analytical limitations:

### Limitations of Current Dataset:
1. **Low Raw Telemetry Channel Diversity**:
   - The Daikibo simulation dataset records only ambient/operating temperature (confined to 23°C - 27°C) alongside status.
   - Real-world electromechanical failures (bearing wear, gear misalignment, motor stator degradation) typically manifest in **vibration spectrum analysis (acceleration g-RMS)**, **motor current signature analysis (MCSA)**, **acoustic emissions**, and **lubricant oil particle counts** before thermal escalation occurs.
2. **Synthetic Data Artifacts**:
   - As identified during data cleaning, telemetry cycles follow repetitive batch loops across 31 iterations. While realistic for operational simulation, true industrial telemetry exhibits seasonal ambient temperature drift and non-stationary wear patterns.
3. **Class Rarity**:
   - With only 103 positive failure labels across the entire month, continuous online model retraining requires active anomaly detection (e.g., Isolation Forests, Autoencoders) rather than purely supervised classification.

### Industrial Deployment Recommendations:
1. **Deploy Multi-Tier Telemetry Gateways**: Augment temperature sensors with high-frequency 3-axis vibration accelerometers on high-risk LaserWelder and LaserCutter spindles.
2. **Dual-Model Architecture**:
   - *Tier 1 (Real-Time Edge)*: Unsupervised Autoencoder / Mahalanobis distance running on local PLC gateways detecting sensor drift.
   - *Tier 2 (Cloud Central)*: Supervised Gradient Boosting model predicting failure probability 2-4 hours ahead of shift changeovers.
3. **Automated CMMS Work Order Dispatch**: Integrate model prediction output with Daikibo's Computerized Maintenance Management System (SAP PM / Maximo) to automatically schedule technician inspection when predicted failure risk exceeds 40%.

