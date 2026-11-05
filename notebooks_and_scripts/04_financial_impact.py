"""
Manufacturing Operations & Predictive Maintenance Analytics
Script 04: Financial Impact Modeling, Cost Quantification & Scenario Analysis
Author: Senior Data Analyst & BI Consultant
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Consulting Dark Navy Palette
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

def run_financial_analysis():
    print("=" * 80)
    print("STEP 4: FINANCIAL IMPACT ANALYSIS & SCENARIO MODELING")
    print("=" * 80)
    
    # Financial Modeling Cost Assumptions (clearly documented)
    financial_rates = {
        "LaserWelder": {"production_loss_per_hr": 1250, "technicians": 2, "tech_rate_per_hr": 120, "scrap_per_incident": 450},
        "LaserCutter": {"production_loss_per_hr": 950, "technicians": 2, "tech_rate_per_hr": 120, "scrap_per_incident": 250},
        "Furnace": {"production_loss_per_hr": 1400, "technicians": 2, "tech_rate_per_hr": 120, "scrap_per_incident": 500},
        "HeavyDutyDrill": {"production_loss_per_hr": 650, "technicians": 1, "tech_rate_per_hr": 120, "scrap_per_incident": 200},
        "ConveyorBelt": {"production_loss_per_hr": 1100, "technicians": 2, "tech_rate_per_hr": 120, "scrap_per_incident": 150},
        "CNC": {"production_loss_per_hr": 800, "technicians": 1, "tech_rate_per_hr": 120, "scrap_per_incident": 200},
        "SpotWelder": {"production_loss_per_hr": 550, "technicians": 1, "tech_rate_per_hr": 120, "scrap_per_incident": 150},
        "MetalPress": {"production_loss_per_hr": 900, "technicians": 2, "tech_rate_per_hr": 120, "scrap_per_incident": 300},
        "AirWrench": {"production_loss_per_hr": 300, "technicians": 1, "tech_rate_per_hr": 120, "scrap_per_incident": 50}
    }
    
    df_rates = pd.DataFrame.from_dict(financial_rates, orient="index").reset_index()
    df_rates.rename(columns={"index": "device_type"}, inplace=True)
    df_rates.to_csv("data/powerbi/dim_financial_assumptions.csv", index=False)
    print("Documented Financial Assumptions Table:")
    print(df_rates.to_string(index=False))
    
    # Load incidents
    incidents = pd.read_csv("data/processed/downtime_incidents.csv")
    
    # Merge rates into incidents
    incidents = incidents.merge(df_rates, on="device_type", how="left")
    
    # Compute financial impact components per incident
    # 1. Lost production capacity
    incidents["lost_production_cost"] = incidents["downtime_hours"] * incidents["production_loss_per_hr"]
    # 2. Direct maintenance & repair labor
    incidents["maintenance_labor_cost"] = incidents["downtime_hours"] * (incidents["technicians"] * incidents["tech_rate_per_hr"])
    # 3. Scrap / WIP spoilage
    incidents["scrap_spoilage_cost"] = incidents["scrap_per_incident"]
    # Total Incident Financial Loss
    incidents["total_financial_loss"] = (
        incidents["lost_production_cost"] + 
        incidents["maintenance_labor_cost"] + 
        incidents["scrap_spoilage_cost"]
    )
    
    incidents.to_csv("data/processed/downtime_incidents.csv", index=False)
    print("\nUpdated downtime_incidents.csv with calculated financial loss fields.")
    
    # -------------------------------------------------------------
    # 1. FINANCIAL LOSS PER FACTORY
    # -------------------------------------------------------------
    factory_finance = incidents.groupby(["factory_code", "factory_name", "country", "city"]).agg(
        total_incidents=("incident_id", "count"),
        total_downtime_hours=("downtime_hours", "sum"),
        lost_production_cost=("lost_production_cost", "sum"),
        maintenance_labor_cost=("maintenance_labor_cost", "sum"),
        scrap_spoilage_cost=("scrap_spoilage_cost", "sum"),
        total_financial_loss=("total_financial_loss", "sum")
    ).reset_index()
    
    # Include zero-cost factories if any (Berlin has 20 min)
    factory_finance = factory_finance.sort_values("total_financial_loss", ascending=False)
    factory_finance["pct_of_global_financial_loss"] = (
        factory_finance["total_financial_loss"] / factory_finance["total_financial_loss"].sum()
    ) * 100.0
    
    print("\n--- Factory Financial Exposure Summary ---")
    print(factory_finance[["factory_name", "total_downtime_hours", "lost_production_cost", "maintenance_labor_cost", "scrap_spoilage_cost", "total_financial_loss", "pct_of_global_financial_loss"]].to_string(index=False))
    factory_finance.to_csv("reports/tables/financial_loss_summary.csv", index=False)
    
    # -------------------------------------------------------------
    # 2. FINANCIAL LOSS PER MACHINE TYPE
    # -------------------------------------------------------------
    machine_finance = incidents.groupby("device_type").agg(
        total_incidents=("incident_id", "count"),
        total_downtime_hours=("downtime_hours", "sum"),
        lost_production_cost=("lost_production_cost", "sum"),
        maintenance_labor_cost=("maintenance_labor_cost", "sum"),
        scrap_spoilage_cost=("scrap_spoilage_cost", "sum"),
        total_financial_loss=("total_financial_loss", "sum")
    ).reset_index().sort_values("total_financial_loss", ascending=False)
    
    print("\n--- Machine-Type Financial Loss Breakdown ---")
    print(machine_finance.to_string(index=False))
    
    # Total monthly loss
    total_loss = factory_finance["total_financial_loss"].sum()
    annualized_loss = total_loss * 12.0
    print(f"\n================================================================================")
    print(f"TOTAL ESTIMATED 31-DAY DOWNTIME LOSS: ${total_loss:,.2f}")
    print(f"ANNUALIZED EXTRAPOLATED IMPACT:        ${annualized_loss:,.2f} / year")
    print(f"================================================================================")
    
    # -------------------------------------------------------------
    # 3. HYPOTHETICAL COST-SAVING SCENARIOS
    # -------------------------------------------------------------
    # Scenario A: Predictive Maintenance (PdM) Early Warning
    # Downtime reduced by 60%, scrap reduced by 40%, labor reduced by 30%
    loss_scenario_a = (
        (factory_finance["lost_production_cost"].sum() * 0.40) +
        (factory_finance["maintenance_labor_cost"].sum() * 0.70) +
        (factory_finance["scrap_spoilage_cost"].sum() * 0.60)
    )
    savings_scenario_a = total_loss - loss_scenario_a
    
    # Scenario B: Rapid Response & Standardized Fast-Swap Spares
    # MTTR reduced by 35% (downtime -35%), labor reduced by 25%, scrap unchanged
    loss_scenario_b = (
        (factory_finance["lost_production_cost"].sum() * 0.65) +
        (factory_finance["maintenance_labor_cost"].sum() * 0.75) +
        (factory_finance["scrap_spoilage_cost"].sum() * 1.00)
    )
    savings_scenario_b = total_loss - loss_scenario_b
    
    # Scenario C: Industry 4.0 Digital Reliability Transformation (Comprehensive)
    # Downtime reduced by 75%, labor reduced by 50%, scrap reduced by 65%
    loss_scenario_c = (
        (factory_finance["lost_production_cost"].sum() * 0.25) +
        (factory_finance["maintenance_labor_cost"].sum() * 0.50) +
        (factory_finance["scrap_spoilage_cost"].sum() * 0.35)
    )
    savings_scenario_c = total_loss - loss_scenario_c
    
    scenarios_df = pd.DataFrame([
        {"Scenario": "Baseline (Current Reactive State)", "Monthly Loss ($)": total_loss, "Monthly Savings ($)": 0.0, "Annualized Savings ($)": 0.0, "Downtime Reduction (%)": 0},
        {"Scenario": "Scenario A: Predictive Telemetry & Early Warning", "Monthly Loss ($)": loss_scenario_a, "Monthly Savings ($)": savings_scenario_a, "Annualized Savings ($)": savings_scenario_a * 12, "Downtime Reduction (%)": 60},
        {"Scenario": "Scenario B: Fast-Swap Spares & Response Teams", "Monthly Loss ($)": loss_scenario_b, "Monthly Savings ($)": savings_scenario_b, "Annualized Savings ($)": savings_scenario_b * 12, "Downtime Reduction (%)": 35},
        {"Scenario": "Scenario C: Industry 4.0 Reliability Transformation", "Monthly Loss ($)": loss_scenario_c, "Monthly Savings ($)": savings_scenario_c, "Annualized Savings ($)": savings_scenario_c * 12, "Downtime Reduction (%)": 75}
    ])
    
    print("\n--- Cost-Saving Scenarios Analysis ---")
    print(scenarios_df.to_string(index=False))
    scenarios_df.to_csv("reports/tables/cost_saving_scenarios.csv", index=False)
    
    # -------------------------------------------------------------
    # FIGURES
    # -------------------------------------------------------------
    # Figure 6: Factory Financial Exposure Breakdown
    fig, ax = setup_consulting_plot(figsize=(10, 5.5))
    
    # Stacked bars for cost components
    bar_width = 0.55
    factories = factory_finance["factory_name"]
    prod_loss = factory_finance["lost_production_cost"]
    maint_loss = factory_finance["maintenance_labor_cost"]
    scrap_loss = factory_finance["scrap_spoilage_cost"]
    
    ax.bar(factories, prod_loss, label="Lost Production Throughput", color=PALETTE["coral"], width=bar_width)
    ax.bar(factories, maint_loss, bottom=prod_loss, label="Emergency Repair Labor", color=PALETTE["cyan"], width=bar_width)
    ax.bar(factories, scrap_loss, bottom=prod_loss + maint_loss, label="Scrap & Spoilage Loss", color=PALETTE["amber"], width=bar_width)
    
    # Total labels
    for i, (tot, pct) in enumerate(zip(factory_finance["total_financial_loss"], factory_finance["pct_of_global_financial_loss"])):
        ax.text(
            i, tot + 250,
            f"${tot:,.0f}\n({pct:.1f}%)",
            ha="center", va="bottom",
            fontsize=10, fontweight="bold",
            color=PALETTE["text_light"]
        )
        
    ax.set_title(f"Factory Financial Exposure by Cost Category (Total: ${total_loss:,.0f})", fontsize=14, fontweight="bold", color=PALETTE["text_light"], pad=16)
    ax.set_ylabel("Estimated Financial Loss ($ USD)", fontsize=11, color=PALETTE["text_muted"])
    ax.set_ylim(0, max(factory_finance["total_financial_loss"]) * 1.25)
    plt.xticks(rotation=10, ha="right", fontsize=10, color=PALETTE["text_light"])
    ax.legend(loc="upper right", framealpha=0.8, facecolor=PALETTE["navy_bg"], edgecolor=PALETTE["grid"])
    plt.tight_layout()
    fig.savefig("reports/figures/06_financial_impact_by_factory.png", dpi=300)
    plt.close()
    
    # Figure 7: Cost Breakdown by Machine Type
    fig, ax = setup_consulting_plot(figsize=(10, 5.5))
    m_types = machine_finance["device_type"]
    m_loss = machine_finance["total_financial_loss"]
    bars = ax.barh(m_types, m_loss, color=PALETTE["teal"], edgecolor=PALETTE["text_light"], linewidth=0.5, height=0.6)
    ax.invert_yaxis()
    
    for bar in bars:
        w = bar.get_width()
        pct = (w / total_loss) * 100.0
        ax.text(
            w + 200, bar.get_y() + bar.get_height() / 2.0,
            f"${w:,.0f} ({pct:.1f}%)",
            va="center", fontsize=9.5, fontweight="bold",
            color=PALETTE["text_light"]
        )
        
    ax.set_title("Machine-Type Financial Loss Attribution ($ USD)", fontsize=14, fontweight="bold", color=PALETTE["text_light"], pad=16)
    ax.set_xlabel("Financial Loss ($ USD)", fontsize=11, color=PALETTE["text_muted"])
    ax.set_xlim(0, max(m_loss) * 1.22)
    plt.tight_layout()
    fig.savefig("reports/figures/07_cost_breakdown_by_machine.png", dpi=300)
    plt.close()
    
    print("\nFinancial Impact Modeling & Figures Successfully Completed.")

if __name__ == "__main__":
    run_financial_analysis()

