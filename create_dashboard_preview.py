"""
Generate Power BI Executive Dashboard 4-Page Visual Layout Graphic
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Corporate dark theme
plt.style.use("dark_background")
fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor="#0B132B")

pages = [
    {
        "title": "PAGE 1: EXECUTIVE OVERVIEW",
        "subtitle": "Global Uptime, Fleet Volume, Critical Outages & Reliability Cockpit",
        "kpis": ["4 Factories", "36 Machines", "160.7k Cycles", "17.17 Hrs Downtime", "99.94% Availability", "29 Incidents"],
        "charts": ["Factory Downtime Ranking (Seiko 480m, SZX 420m)", "Downtime by Machine Type (LaserWelder 46.6%)", "31-Day Timeline Trend (Day 15 Spike)", "Global Facilities Geo Map (4 Plants)"]
    },
    {
        "title": "PAGE 2: FACTORY PERFORMANCE",
        "subtitle": "Cross-Plant Reliability Benchmarking, Shift Variance & Regional Diagnostics",
        "kpis": ["Berlin: 99.995% (Benchmark)", "Meiyo: 99.973%", "Shenzhen: 99.895%", "Seiko: 99.881% (Lowest)"],
        "charts": ["Factory Section Breakdown (SZX Sec 3: 410m)", "Shift Downtime Matrix (Morning: 58.3%)", "Operational Scorecard Matrix (MTBF/MTTR)", "Daily Comparative Production Trajectory"]
    },
    {
        "title": "PAGE 3: MACHINE ANALYTICS & RELIABILITY",
        "subtitle": "Asset Health Diagnostics, MTBF vs MTTR Matrix & Failure Archetypes",
        "kpis": ["Fleet Health: 99.2%", "Avg MTBF: 923.6 Hrs", "Avg MTTR: 35.5 Mins", "Chronic Asset: LaserCutter (23 inc)"],
        "charts": ["Reliability Matrix (MTBF vs MTTR Quadrants)", "Failure Incident Frequency (LaserCutter 79%)", "Failure Severity (1 Catastrophic, 1 Major, 27 Minor)", "Detailed Maintenance Incident Log Table"]
    },
    {
        "title": "PAGE 4: FINANCIAL IMPACT & RISK",
        "subtitle": "Cost Quantification, Scrap Exposure & Predictive ROI Scenario Simulator",
        "kpis": ["$29,792.50 Monthly Loss", "$357,510 Annualized", "$18.45k Lost Throughput", "$7.4k Scrap Loss"],
        "charts": ["Financial Exposure by Factory (SZX $14.0k)", "Cost by Machine Type (Lasers = 89.5%)", "Interactive What-If Slicer (0-100% Reduction)", "Strategic Scenarios (C: $247.4k Annual Savings)"]
    }
]

for idx, (ax, p) in enumerate(zip(axes.flat, pages)):
    ax.set_facecolor("#1C2541")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    
    # Outer Card Border
    rect = patches.FancyBboxPatch((1, 1), 98, 98, boxstyle="round,pad=1.5", edgecolor="#2D3748", facecolor="#1C2541", linewidth=1.5)
    ax.add_patch(rect)
    
    # Header bar
    hdr = patches.Rectangle((2, 86), 96, 12, facecolor="#0F172A", edgecolor="none")
    ax.add_patch(hdr)
    
    ax.text(4, 93, p["title"], fontsize=12, fontweight="bold", color="#00F2FE", va="center")
    ax.text(4, 88.5, p["subtitle"], fontsize=8.5, color="#94A3B8", va="center")
    
    # KPI Strip
    kpi_bar = patches.Rectangle((3, 73), 94, 11, facecolor="#1E293B", edgecolor="#334155", linewidth=0.8)
    ax.add_patch(kpi_bar)
    
    step = 94 / len(p["kpis"])
    for ki, kpi_text in enumerate(p["kpis"]):
        x_pos = 4 + (ki * step) + (step / 2)
        ax.text(x_pos, 78.5, kpi_text, fontsize=8, fontweight="bold", color="#F8FAFC", ha="center", va="center")
        
    # Visual Quadrants
    quads = [
        ((4, 42), 44, 28, p["charts"][0]),
        ((52, 42), 44, 28, p["charts"][1]),
        ((4, 8), 44, 30, p["charts"][2]),
        ((52, 8), 44, 30, p["charts"][3])
    ]
    
    for (qx, qy), qw, qh, qtext in quads:
        box = patches.FancyBboxPatch((qx, qy), qw, qh, boxstyle="round,pad=0.8", facecolor="#0B132B", edgecolor="#334155", linewidth=0.8)
        ax.add_patch(box)
        # Small accent bar
        acc = patches.Rectangle((qx, qy + qh - 3), qw, 3, facecolor="#00F2FE" if (qx+qy)%2==0 else "#4FACFE")
        ax.add_patch(acc)
        ax.text(qx + 2, qy + qh - 6, qtext, fontsize=7.5, fontweight="bold", color="#F8FAFC", va="top")
        
plt.suptitle("DAIKIBO INDUSTRIALS | 4-PAGE ENTERPRISE POWER BI DASHBOARD ARCHITECTURE", fontsize=16, fontweight="bold", color="#F8FAFC", y=0.98)
plt.tight_layout()
os.makedirs("reports/figures", exist_ok=True)
fig.savefig("reports/figures/10_powerbi_dashboard_preview.png", dpi=300)
plt.close()
print("Generated reports/figures/10_powerbi_dashboard_preview.png successfully.")

