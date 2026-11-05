"""
Manufacturing Operations & Predictive Maintenance Analytics
Script 05: Predictive Modeling, Feature Engineering & Risk Classification
Author: Senior Data Analyst & BI Consultant
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score
)

# Consulting Dark Navy Theme
plt.style.use("dark_background")
PALETTE = {
    "navy_bg": "#0B132B",
    "card_bg": "#1C2541",
    "teal": "#00F2FE",
    "cyan": "#4FACFE",
    "emerald": "#10B981",
    "amber": "#F59E0B",
    "coral": "#F43F5E",
    "text_light": "#F8FAFC",
    "text_muted": "#94A3B8",
    "grid": "#2D3748"
}

def setup_consulting_plot(figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=PALETTE["navy_bg"])
    ax.set_facecolor(PALETTE["card_bg"])
    ax.grid(color=PALETTE["grid"], linestyle="--", linewidth=0.6, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color(PALETTE["grid"])
    return fig, ax

def run_predictive_modeling():
    print("=" * 80)
    print("STEP 5: PREDICTIVE MAINTENANCE MODELING & EVALUATION")
    print("=" * 80)
    
    # Load clean data
    df = pd.read_csv("data/processed/daikibo_telemetry_clean.csv")
    df = df.sort_values(["device_id", "block_id", "hour", "raw_timestamp"]).reset_index(drop=True)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution (is_unhealthy):")
    print(df["is_unhealthy"].value_counts())
    print(f"Positive class prevalence: {(df['is_unhealthy'].sum() / len(df)) * 100:.4f}%")
    
    # -------------------------------------------------------------
    # 1. FEATURE ENGINEERING
    # -------------------------------------------------------------
    print("\nEngineering temporal and sensor telemetry features...")
    
    # Rolling sensor metrics per device
    df["temp_rolling_mean_6"] = df.groupby("device_id")["temperature_c"].transform(lambda x: x.rolling(6, min_periods=1).mean())
    df["temp_rolling_std_6"] = df.groupby("device_id")["temperature_c"].transform(lambda x: x.rolling(6, min_periods=1).std()).fillna(0)
    df["temp_diff_prev"] = df.groupby("device_id")["temperature_c"].diff().fillna(0)
    
    # Operating time within daily simulation block (hours elapsed)
    df["block_step"] = df.groupby(["device_id", "block_id"]).cumcount()
    df["operating_hours_in_batch"] = (df["block_step"] * 10) / 60.0
    
    # Cyclical encoding of hour
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)
    
    # Categorical One-Hot Encoding
    feature_cols = [
        "temperature_c", "temp_rolling_mean_6", "temp_rolling_std_6", "temp_diff_prev",
        "operating_hours_in_batch", "hour_sin", "hour_cos", "day_of_month"
    ]
    
    cat_cols = ["device_type", "factory_code", "section", "shift"]
    df_encoded = pd.get_dummies(df[feature_cols + cat_cols], columns=cat_cols, drop_first=True)
    
    X = df_encoded
    y = df["is_unhealthy"]
    
    print(f"Feature matrix X shape: {X.shape}")
    
    # Train / Test Stratified Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training set: {X_train.shape[0]:,} samples ({y_train.sum()} failures)")
    print(f"Test set:     {X_test.shape[0]:,} samples ({y_test.sum()} failures)")
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # -------------------------------------------------------------
    # 2. MODEL TRAINING & COMPARISON
    # -------------------------------------------------------------
    models = {
        "Balanced Logistic Regression": LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        ),
        "Balanced Random Forest": RandomForestClassifier(
            n_estimators=100, class_weight="balanced_subsample",
            max_depth=12, min_samples_split=10, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting Classifier": GradientBoostingClassifier(
            n_estimators=100, max_depth=5, learning_rate=0.08, random_state=42
        )
    }
    
    results = []
    trained_models = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        if "Logistic" in name:
            model.fit(X_train_scaled, y_train)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            y_pred = (y_pred_proba >= 0.5).astype(int)
        else:
            model.fit(X_train, y_train)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            y_pred = (y_pred_proba >= 0.5).astype(int)
            
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        pr_auc = average_precision_score(y_test, y_pred_proba)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        trained_models[name] = {"model": model, "y_pred_proba": y_pred_proba, "y_pred": y_pred}
        
        results.append({
            "Model Name": name,
            "ROC-AUC": round(roc_auc, 4),
            "PR-AUC (Avg Precision)": round(pr_auc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4)
        })
        
    df_results = pd.DataFrame(results)
    print("\n--- Predictive Model Performance Comparison ---")
    print(df_results.to_string(index=False))
    df_results.to_csv("reports/tables/predictive_model_results.csv", index=False)
    
    # Best model is Random Forest
    rf_pack = trained_models["Balanced Random Forest"]
    rf_model = rf_pack["model"]
    y_pred_proba_rf = rf_pack["y_pred_proba"]
    y_pred_rf = rf_pack["y_pred"]
    
    print("\nClassification Report (Balanced Random Forest):")
    print(classification_report(y_test, y_pred_rf, target_names=["Healthy", "Unhealthy"]))
    
    # -------------------------------------------------------------
    # 3. VISUALIZATIONS: ROC & PRECISION-RECALL CURVES
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=PALETTE["navy_bg"])
    for ax in [ax1, ax2]:
        ax.set_facecolor(PALETTE["card_bg"])
        ax.grid(color=PALETTE["grid"], linestyle="--", linewidth=0.6, alpha=0.7)
        for spine in ax.spines.values():
            spine.set_color(PALETTE["grid"])
            
    # ROC Curves
    colors = [PALETTE["amber"], PALETTE["teal"], PALETTE["cyan"]]
    for (name, pack), c in zip(trained_models.items(), colors):
        fpr, tpr, _ = roc_curve(y_test, pack["y_pred_proba"])
        score = roc_auc_score(y_test, pack["y_pred_proba"])
        ax1.plot(fpr, tpr, label=f"{name} (AUC={score:.3f})", color=c, linewidth=2.0)
        
    ax1.plot([0, 1], [0, 1], linestyle="--", color=PALETTE["text_muted"], alpha=0.6)
    ax1.set_title("Receiver Operating Characteristic (ROC)", fontsize=13, fontweight="bold", color=PALETTE["text_light"], pad=14)
    ax1.set_xlabel("False Positive Rate", fontsize=11, color=PALETTE["text_muted"])
    ax1.set_ylabel("True Positive Rate (Recall)", fontsize=11, color=PALETTE["text_muted"])
    ax1.legend(loc="lower right", framealpha=0.8, facecolor=PALETTE["navy_bg"])
    
    # Precision-Recall Curves
    for (name, pack), c in zip(trained_models.items(), colors):
        prec_curve, rec_curve, _ = precision_recall_curve(y_test, pack["y_pred_proba"])
        pr_score = average_precision_score(y_test, pack["y_pred_proba"])
        ax2.plot(rec_curve, prec_curve, label=f"{name} (PR-AUC={pr_score:.3f})", color=c, linewidth=2.0)
        
    ax2.set_title("Precision-Recall (PR) Curve (Rare Class Focus)", fontsize=13, fontweight="bold", color=PALETTE["text_light"], pad=14)
    ax2.set_xlabel("Recall", fontsize=11, color=PALETTE["text_muted"])
    ax2.set_ylabel("Precision", fontsize=11, color=PALETTE["text_muted"])
    ax2.legend(loc="upper right", framealpha=0.8, facecolor=PALETTE["navy_bg"])
    
    plt.tight_layout()
    fig.savefig("reports/figures/08_predictive_model_roc_pr_curve.png", dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # 4. CONFUSION MATRIX & FEATURE IMPORTANCE
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=PALETTE["navy_bg"])
    for ax in [ax1, ax2]:
        ax.set_facecolor(PALETTE["card_bg"])
        ax.grid(color=PALETTE["grid"], linestyle="--", linewidth=0.6, alpha=0.7)
        for spine in ax.spines.values():
            spine.set_color(PALETTE["grid"])
            
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred_rf)
    sns.heatmap(
        cm, annot=True, fmt=",d", cmap=sns.dark_palette(PALETTE["teal"], as_cmap=True),
        xticklabels=["Predicted Healthy", "Predicted Unhealthy"],
        yticklabels=["Actual Healthy", "Actual Unhealthy"],
        ax=ax1, cbar=False, annot_kws={"fontsize": 12, "fontweight": "bold"}
    )
    ax1.set_title("Random Forest Confusion Matrix", fontsize=13, fontweight="bold", color=PALETTE["text_light"], pad=14)
    
    # Feature Importance (Top 10)
    importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
    
    bars = ax2.barh(importances.index, importances.values, color=PALETTE["cyan"], edgecolor=PALETTE["teal"], height=0.6)
    ax2.invert_yaxis()
    ax2.set_title("Top 10 Predictive Failure Risk Drivers", fontsize=13, fontweight="bold", color=PALETTE["text_light"], pad=14)
    ax2.set_xlabel("Feature Importance Gini Score", fontsize=11, color=PALETTE["text_muted"])
    
    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 0.005, bar.get_y() + bar.get_height() / 2.0, f"{w:.3f}", va="center", fontsize=9.5, fontweight="bold", color=PALETTE["text_light"])
        
    ax2.set_xlim(0, max(importances.values) * 1.25)
    plt.tight_layout()
    fig.savefig("reports/figures/09_confusion_matrix_feature_importance.png", dpi=300)
    plt.close()
    
    print("\nPredictive Maintenance Modeling Successfully Completed.")

if __name__ == "__main__":
    run_predictive_modeling()

