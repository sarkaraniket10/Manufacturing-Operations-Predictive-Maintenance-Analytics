"""
Manufacturing Operations & Predictive Maintenance Analytics
Script 02: Comprehensive Exploratory Data Analysis & Visualizations
Author: Senior Data Analyst & BI Consultant
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Consulting Dark Navy Enterprise Styling
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

def run_eda():
    print("=" * 80)
    print("STEP 2: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 80)
    
    df = pd.read_csv("data/processed/daikibo_telemetry_clean.csv")
    incidents = pd.read_csv("data/processed/downtime_incidents.csv")
    daily = pd.read_csv("data/processed/factory_daily_summary.csv")
    machines = pd.read_csv("data/processed/machine_health_summary.csv")
    
    os.makedirs("reports/figures", exist_ok=True)
    os.makedirs("reports/tables", exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. FACTORY-WISE DOWNTIME ANALYSIS
    # -------------------------------------------------------------
    print("\n--- 1. FACTORY-WISE DOWNTIME & RELIABILITY ---")
    factory_kpis = df.groupby(["factory_code", "factory_name", "country", "city"]).agg(
        total_records=("status", "count"),
        healthy_events=("status", lambda x: (x == "Healthy").sum()),
        unhealthy_events=("status", lambda x: (x == "Unhealthy").sum()),
        total_downtime_mins=("downtime_minutes", "sum")
    ).reset_index()
    
    factory_kpis["downtime_hours"] = factory_kpis["total_downtime_mins"] / 60.0
    factory_kpis["planned_hours"] = (factory_kpis["total_records"] * 10) / 60.0
    factory_kpis["availability_pct"] = (
        (factory_kpis["planned_hours"] - factory_kpis["downtime_hours"]) / factory_kpis["planned_hours"]
    ) * 100.0
    factory_kpis["downtime_share_pct"] = (
        factory_kpis["total_downtime_mins"] / factory_kpis["total_downtime_mins"].sum()
    ) * 100.0
    
    # Add incident counts
    inc_by_factory = incidents.groupby("factory_code")["incident_id"].count().reset_index()
    inc_by_factory.rename(columns={"incident_id": "total_incidents"}, inplace=True)
    factory_kpis = factory_kpis.merge(inc_by_factory, on="factory_code", how="left").fillna(0)
    factory_kpis["total_incidents"] = factory_kpis["total_incidents"].astype(int)
    
    # Sort by downtime descending
    factory_kpis = factory_kpis.sort_values("total_downtime_mins", ascending=False)
    factory_kpis.to_csv("reports/tables/factory_performance_kpis.csv", index=False)
    print(factory_kpis[["factory_name", "total_downtime_mins", "downtime_hours", "availability_pct", "total_incidents", "downtime_share_pct"]].to_string())
    
    # Figure 1: Factory Downtime Distribution
    fig, ax = setup_consulting_plot(figsize=(10, 5.5))
    bars = ax.bar(
        factory_kpis["factory_name"],
        factory_kpis["total_downtime_mins"],
        color=[PALETTE["coral"], PALETTE["amber"], PALETTE["teal"], PALETTE["emerald"]],
        width=0.55,
        edgecolor=PALETTE["text_light"],
        linewidth=0.5
    )
    
    # Direct data labeling
    for bar in bars:
        yval = bar.get_height()
        hours = yval / 60.0
        pct = (yval / factory_kpis["total_downtime_mins"].sum()) * 100.0
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 12,
            f"{int(yval)} min\n({hours:.1f} hrs | {pct:.1f}%)",
            ha="center", va="bottom",
            fontsize=10, fontweight="bold",
            color=PALETTE["text_light"]
        )
        
    ax.set_title("Factory Equipment Downtime Distribution (Total: 1,030 mins)", fontsize=14, fontweight="bold", color=PALETTE["text_light"], pad=18)
    ax.set_ylabel("Downtime (Minutes)", fontsize=11, color=PALETTE["text_muted"])
    ax.set_ylim(0, 560)
    plt.xticks(rotation=10, ha="right", fontsize=10, color=PALETTE["text_light"])
    plt.tight_layout()
    fig.savefig("reports/figures/01_factory_downtime_distribution.png", dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # 2. MACHINE-TYPE PERFORMANCE ANALYSIS
    # -------------------------------------------------------------
    print("\n--- 2. MACHINE-TYPE PERFORMANCE ANALYSIS ---")
    machine_kpis = df.groupby("device_type").agg(
        total_records=("status", "count"),
        unhealthy_events=("status", lambda x: (x == "Unhealthy").sum()),
        total_downtime_mins=("downtime_minutes", "sum")
    ).reset_index()
    
    machine_kpis["downtime_hours"] = machine_kpis["total_downtime_mins"] / 60.0
    machine_kpis["downtime_share_pct"] = (
        machine_kpis["total_downtime_mins"] / machine_kpis["total_downtime_mins"].sum()
    ) * 100.0
    
    inc_by_dev = incidents.groupby("device_type")["incident_id"].count().reset_index()
    inc_by_dev.rename(columns={"incident_id": "failure_incidents"}, inplace=True)
    machine_kpis = machine_kpis.merge(inc_by_dev, on="device_type", how="left").fillna(0)
    machine_kpis["failure_incidents"] = machine_kpis["failure_incidents"].astype(int)
    machine_kpis = machine_kpis.sort_values("total_downtime_mins", ascending=False)
    
    machine_kpis.to_csv("reports/tables/machine_failure_metrics.csv", index=False)
    print(machine_kpis[["device_type", "total_downtime_mins", "downtime_hours", "failure_incidents", "downtime_share_pct"]].to_string())
    
    # Figure 2: Machine Type Downtime & Failure Frequency
    fig, ax1 = setup_consulting_plot(figsize=(11, 6))
    
    y_pos = np.arange(len(machine_kpis))
    bars = ax1.barh(
        y_pos,
        machine_kpis["total_downtime_mins"],
        color=PALETTE["cyan"],
        height=0.6,
        edgecolor=PALETTE["teal"],
        alpha=0.9
    )
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(machine_kpis["device_type"], fontsize=10, color=PALETTE["text_light"])
    ax1.invert_yaxis()  # Top down
    ax1.set_xlabel("Downtime (Minutes)", fontsize=11, color=PALETTE["text_muted"])
    ax1.set_title("Equipment Downtime by Machine Type with Failure Incident Frequency", fontsize=14, fontweight="bold", color=PALETTE["text_light"], pad=16)
    
    # Add annotations with incident count
    for idx, (bar, inc_count, mins) in enumerate(zip(bars, machine_kpis["failure_incidents"], machine_kpis["total_downtime_mins"])):
        if mins > 0:
            ax1.text(
                mins + 10,
                bar.get_y() + bar.get_height() / 2.0,
                f"{mins} min ({mins/60.0:.1f} hrs) | {inc_count} incident{'s' if inc_count>1 else ''}",
                va="center", fontsize=9.5, fontweight="bold",
                color=PALETTE["text_light"]
            )
        else:
            ax1.text(
                10,
                bar.get_y() + bar.get_height() / 2.0,
                "0 min (100% Uptime)",
                va="center", fontsize=9, fontstyle="italic",
                color=PALETTE["emerald"]
            )
            
    ax1.set_xlim(0, 560)
    plt.tight_layout()
    fig.savefig("reports/figures/02_machine_type_downtime_breakdown.png", dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # 3. HEATMAP: FACTORY VS MACHINE TYPE MATRIX
    # -------------------------------------------------------------
    print("\n--- 3. FACTORY VS MACHINE TYPE MATRIX ---")
    matrix = df.groupby(["factory_name", "device_type"])["downtime_minutes"].sum().unstack().fillna(0)
    
    fig, ax = setup_consulting_plot(figsize=(11, 5.5))
    cmap = sns.dark_palette(PALETTE["teal"], as_cmap=True)
    sns.heatmap(
        matrix,
        annot=True,
        fmt=".0f",
        cmap=cmap,
        linewidths=1.0,
        linecolor=PALETTE["navy_bg"],
        cbar_kws={"label": "Downtime Minutes"},
        ax=ax,
        annot_kws={"fontsize": 10, "fontweight": "bold"}
    )
    
    ax.set_title("Manufacturing Downtime Heatmap: Factory Location vs Equipment Type (Mins)", fontsize=13, fontweight="bold", color=PALETTE["text_light"], pad=16)
    ax.set_xlabel("Equipment Type", fontsize=11, color=PALETTE["text_muted"])
    ax.set_ylabel("Factory Location", fontsize=11, color=PALETTE["text_muted"])
    plt.xticks(rotation=30, ha="right", fontsize=9.5, color=PALETTE["text_light"])
    plt.yticks(rotation=0, fontsize=10, color=PALETTE["text_light"])
    plt.tight_layout()
    fig.savefig("reports/figures/03_factory_machine_heatmap.png", dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # 4. DAILY DOWNTIME TIMELINE TREND (Days 1 to 31)
    # -------------------------------------------------------------
    print("\n--- 4. DAILY OPERATIONAL DOWNTIME TRENDS ---")
    daily_trend = df.groupby(["day_of_month", "factory_name"])["downtime_minutes"].sum().unstack().fillna(0)
    
    fig, ax = setup_consulting_plot(figsize=(12, 5.5))
    
    # Stacked bar chart for daily downtime
    factory_colors = {
        "Factory Seiko (Osaka)": PALETTE["coral"],
        "Shenzhen Plant (China)": PALETTE["amber"],
        "Factory Meiyo (Tokyo)": PALETTE["teal"],
        "Berlin Facility (Germany)": PALETTE["emerald"]
    }
    
    bottom = np.zeros(len(daily_trend))
    for col in ["Factory Seiko (Osaka)", "Shenzhen Plant (China)", "Factory Meiyo (Tokyo)", "Berlin Facility (Germany)"]:
        if col in daily_trend.columns:
            values = daily_trend[col].values
            ax.bar(
                daily_trend.index,
                values,
                bottom=bottom,
                label=col,
                color=factory_colors[col],
                width=0.7,
                alpha=0.9
            )
            bottom += values
            
    ax.set_title("31-Day Operational Downtime Timeline Across Manufacturing Sites", fontsize=14, fontweight="bold", color=PALETTE["text_light"], pad=16)
    ax.set_xlabel("Day of Operational Month (1 - 31)", fontsize=11, color=PALETTE["text_muted"])
    ax.set_ylabel("Total Daily Downtime (Minutes)", fontsize=11, color=PALETTE["text_muted"])
    ax.set_xticks(range(1, 32, 2))
    ax.legend(loc="upper left", framealpha=0.8, facecolor=PALETTE["navy_bg"], edgecolor=PALETTE["grid"])
    
    # Highlight major spikes
    ax.annotate(
        "Day 15: Catastrophic 8-hr\nLaserWelder Outage (Seiko)",
        xy=(15, 480), xytext=(17, 430),
        arrowprops=dict(facecolor=PALETTE["coral"], shrink=0.08, width=1.5, headwidth=6),
        fontsize=9.5, fontweight="bold", color=PALETTE["coral"]
    )
    
    ax.annotate(
        "Day 27: HeavyDutyDrill Breakdown\n(Meiyo - 70 mins)",
        xy=(27, 70), xytext=(22, 120),
        arrowprops=dict(facecolor=PALETTE["teal"], shrink=0.08, width=1.5, headwidth=6),
        fontsize=9, fontweight="bold", color=PALETTE["teal"]
    )
    
    plt.tight_layout()
    fig.savefig("reports/figures/04_daily_downtime_timeline.png", dpi=300)
    plt.close()
    
    # -------------------------------------------------------------
    # 5. SHIFT & SECTION DOWNTIME ANALYSIS
    # -------------------------------------------------------------
    print("\n--- 5. SHIFT & SECTION PERFORMANCE ---")
    shift_summary = df.groupby(["shift", "factory_name"])["downtime_minutes"].sum().unstack().fillna(0)
    print("Shift Downtime Breakdown (Mins):")
    print(shift_summary)
    
    section_summary = df.groupby(["section", "factory_name"])["downtime_minutes"].sum().unstack().fillna(0)
    print("\nSection Downtime Breakdown (Mins):")
    print(section_summary)
    
    print("\nEDA Phase Successfully Completed. Generated 4 high-resolution consulting figures.")

if __name__ == "__main__":
    run_eda()

