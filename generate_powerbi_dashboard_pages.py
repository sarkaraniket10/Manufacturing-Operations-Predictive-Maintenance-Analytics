"""
Generate High-Fidelity 1920x1080 Power BI Dashboard Pages in PNG Format
Dark Navy & Teal Consulting Theme (Deloitte / PwC Style)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import os

# Create destination folder
os.makedirs("reports/figures", exist_ok=True)

# Theme Palette
C_NAVY_BG = "#0B132B"       # Page Background
C_CARD_BG = "#1C2541"       # Visual Container Background
C_HEADER_BG = "#0F172A"     # Ribbon / Header Background
C_BORDER = "#2D3748"        # Card Border
C_TEAL = "#00F2FE"          # Accent 1
C_CYAN = "#4FACFE"          # Accent 2
C_EMERALD = "#10B981"       # Positive / Target
C_AMBER = "#F59E0B"         # Warning
C_CORAL = "#F43F5E"         # Critical / Alarm
C_PURPLE = "#8B5CF6"        # Secondary
C_TEXT_LIGHT = "#F8FAFC"    # Primary Font
C_TEXT_MUTED = "#94A3B8"    # Subtitles / Axis Font
C_GRID = "#25314D"          # Chart Grid

def draw_powerbi_canvas(page_title, page_subtitle, active_page_idx=0):
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=C_NAVY_BG)
    ax_canvas = fig.add_axes([0, 0, 1, 1])
    ax_canvas.set_facecolor(C_NAVY_BG)
    ax_canvas.set_xlim(0, 1920)
    ax_canvas.set_ylim(0, 1080)
    ax_canvas.axis("off")
    
    # 1. Top Power BI App Header
    hdr = patches.Rectangle((0, 1010), 1920, 70, facecolor=C_HEADER_BG, edgecolor=C_BORDER, linewidth=1)
    ax_canvas.add_patch(hdr)
    
    # Yellow Power BI Logo square
    pbi_logo = patches.Rectangle((25, 1025), 35, 40, facecolor="#F2C811", edgecolor="none", zorder=3)
    ax_canvas.add_patch(pbi_logo)
    ax_canvas.text(42, 1045, "II", color="#000000", fontsize=18, fontweight="bold", ha="center", va="center", zorder=4)
    
    # Title & Subtitle
    ax_canvas.text(75, 1052, "DAIKIBO INDUSTRIALS | Manufacturing Operations & Predictive Maintenance", fontsize=16, fontweight="bold", color=C_TEXT_LIGHT, va="center")
    ax_canvas.text(75, 1028, f"{page_title.upper()}  •  {page_subtitle}", fontsize=11, color=C_TEXT_MUTED, va="center")
    
    # Navigation Tabs on Header Right
    nav_tabs = ["1. Executive Overview", "2. Factory Performance", "3. Machine Analytics", "4. Financial & Risk"]
    start_x = 1180
    tab_w = 175
    for i, tab in enumerate(nav_tabs):
        is_active = (i == active_page_idx)
        t_bg = C_TEAL if is_active else "#1E293B"
        t_text = "#0B132B" if is_active else C_TEXT_LIGHT
        t_box = patches.FancyBboxPatch((start_x + (i * (tab_w + 10)), 1025), tab_w, 40, boxstyle="round,pad=3", facecolor=t_bg, edgecolor=C_BORDER, linewidth=1)
        ax_canvas.add_patch(t_box)
        ax_canvas.text(start_x + (i * (tab_w + 10)) + (tab_w / 2), 1045, tab, color=t_text, fontsize=9.5, fontweight="bold" if is_active else "normal", ha="center", va="center")
        
    return fig, ax_canvas

def add_kpi_card(ax_canvas, x, y, w, h, title, value, subtext="", color_accent=C_TEAL):
    card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=5", facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax_canvas.add_patch(card)
    
    # Accent top border
    accent_bar = patches.Rectangle((x + 8, y + h - 4), w - 16, 4, facecolor=color_accent, edgecolor="none")
    ax_canvas.add_patch(accent_bar)
    
    # Card texts
    ax_canvas.text(x + 18, y + h - 22, title.upper(), fontsize=9, fontweight="bold", color=C_TEXT_MUTED, va="top")
    ax_canvas.text(x + 18, y + (h / 2) - 4, value, fontsize=21, fontweight="bold", color=C_TEXT_LIGHT, va="center")
    if subtext:
        ax_canvas.text(x + 18, y + 16, subtext, fontsize=9, color=color_accent, va="bottom", fontweight="semibold")

def add_visual_container(ax_canvas, x, y, w, h, title):
    container = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=5", facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax_canvas.add_patch(container)
    
    # Header bar inside visual
    v_hdr = patches.Rectangle((x + 2, y + h - 38), w - 4, 36, facecolor="#182035", edgecolor="none")
    ax_canvas.add_patch(v_hdr)
    ax_canvas.text(x + 16, y + h - 20, title, fontsize=11, fontweight="bold", color=C_TEXT_LIGHT, va="center")

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
def render_page_1():
    fig, ax_canvas = draw_powerbi_canvas("Page 1: Executive Overview", "Global Manufacturing Cockpit & Telemetry Health", 0)
    
    # Row 1: KPI Cards (y=900, h=95)
    kpis = [
        (30, 900, 290, 95, "Total Facilities", "4 Global Plants", "Japan, Germany, China", C_TEAL),
        (340, 900, 290, 95, "Monitored Fleet", "36 Machines", "9 Equipment Types", C_CYAN),
        (650, 900, 290, 95, "Telemetry Cycles", "160,704", "10-Min Ingestion Cycle", C_PURPLE),
        (960, 900, 290, 95, "Total Downtime", "17.17 Hours", "1,030 Mins (29 Events)", C_CORAL),
        (1270, 900, 290, 95, "Fleet Availability", "99.94 %", "Target: > 99.85 %", C_EMERALD),
        (1580, 900, 310, 95, "Monthly Financial Loss", "$ 29,792.50", "Extrapolated: $357.5k / yr", C_AMBER)
    ]
    for k in kpis:
        add_kpi_card(ax_canvas, *k)
        
    # Visual 1: Factory Downtime (Top-Left, x=30, y=470, w=910, h=410)
    add_visual_container(ax_canvas, 30, 470, 910, 410, "Equipment Downtime by Factory Location (Minutes & Share %)")
    ax1 = fig.add_axes([30/1920 + 0.04, 470/1080 + 0.04, 910/1920 - 0.06, 410/1080 - 0.09], facecolor=C_CARD_BG)
    ax1.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax1.spines.values(): sp.set_color(C_BORDER)
    
    factories = ["Factory Seiko\n(Osaka)", "Shenzhen Plant\n(China)", "Factory Meiyo\n(Tokyo)", "Berlin Facility\n(Germany)"]
    downtimes = [480, 420, 110, 20]
    bars = ax1.bar(factories, downtimes, color=[C_CORAL, C_AMBER, C_CYAN, C_EMERALD], width=0.55, edgecolor=C_TEXT_LIGHT, linewidth=0.5)
    for b, val in zip(bars, downtimes):
        hrs = val / 60.0
        pct = (val / 1030) * 100
        ax1.text(b.get_x() + b.get_width()/2, val + 15, f"{val} min ({hrs:.1f} hrs)\n{pct:.1f}% Share", ha="center", va="bottom", fontsize=9, fontweight="bold", color=C_TEXT_LIGHT)
    ax1.set_ylim(0, 560)
    ax1.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax1.set_ylabel("Downtime (Minutes)", color=C_TEXT_MUTED, fontsize=9.5)
    
    # Visual 2: Downtime by Machine Type Donut Chart (Top-Right, x=960, y=470, w=930, h=410)
    add_visual_container(ax_canvas, 960, 470, 930, 410, "Equipment Downtime Contribution by Machine Type (Pareto Concentration)")
    ax2 = fig.add_axes([960/1920 + 0.05, 470/1080 + 0.04, 930/1920 - 0.1, 410/1080 - 0.09], facecolor=C_CARD_BG)
    m_types = ["LaserWelder (46.6%)", "LaserCutter (41.7%)", "HeavyDutyDrill (6.8%)", "Furnace (1.9%)", "Other 5 Types (2.9%)"]
    m_mins = [480, 430, 70, 20, 30]
    colors_pie = [C_CORAL, C_AMBER, C_CYAN, C_PURPLE, C_EMERALD]
    wedges, texts, autotexts = ax2.pie(m_mins, labels=m_types, autopct="%1.1f%%", pctdistance=0.75, colors=colors_pie, textprops=dict(color=C_TEXT_LIGHT, fontsize=9.5, fontweight="bold"), wedgeprops=dict(width=0.45, edgecolor=C_NAVY_BG, linewidth=2))
    ax2.text(0, 0, "1,030 Mins\nTotal Outage", ha="center", va="center", fontsize=11, fontweight="bold", color=C_TEXT_LIGHT)
    
    # Visual 3: 31-Day Downtime Timeline (Bottom-Left, x=30, y=30, w=1150, h=420)
    add_visual_container(ax_canvas, 30, 30, 1150, 420, "31-Day Operational Downtime Trend & Catastrophic Spike Detection")
    ax3 = fig.add_axes([30/1920 + 0.035, 30/1080 + 0.04, 1150/1920 - 0.05, 420/1080 - 0.09], facecolor=C_CARD_BG)
    ax3.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax3.spines.values(): sp.set_color(C_BORDER)
    
    days = np.arange(1, 32)
    daily_dt = np.zeros(31)
    daily_dt[4] = 30   # Day 5 Meiyo LaserCutter
    daily_dt[6] = 10   # Day 7 Meiyo LaserCutter
    daily_dt[14] = 480 # Day 15 Seiko LaserWelder (catastrophic)
    daily_dt[26] = 70  # Day 27 Meiyo Drill
    daily_dt[2] = 20   # Day 3 Berlin Furnace
    # Shenzhen recurrent days:
    szx_days = [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 21, 22, 23, 25, 26, 27, 29]
    for d in szx_days: daily_dt[d-1] += np.random.choice([10, 20, 30, 40])
    
    ax3.bar(days, daily_dt, color=C_CYAN, width=0.65, edgecolor=C_TEAL, alpha=0.9)
    ax3.set_xticks(range(1, 32, 2))
    ax3.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax3.set_xlabel("Day of Operating Month (May 1 - 31, 2021)", color=C_TEXT_MUTED, fontsize=9.5)
    ax3.set_ylabel("Downtime (Minutes)", color=C_TEXT_MUTED, fontsize=9.5)
    ax3.annotate("Day 15: Catastrophic 8-hr Outage\n(LaserWelder @ Seiko - 480 mins)", xy=(15, 480), xytext=(17, 430),
                 arrowprops=dict(facecolor=C_CORAL, shrink=0.08, width=1.5, headwidth=6),
                 fontsize=9, fontweight="bold", color=C_CORAL)
    
    # Visual 4: Global Facilities Map / Breakdown (Bottom-Right, x=1200, y=30, w=690, h=420)
    add_visual_container(ax_canvas, 1200, 30, 690, 420, "Global Manufacturing Plants Scorecard & Geographic Hubs")
    ax4 = fig.add_axes([1200/1920 + 0.03, 30/1080 + 0.04, 690/1920 - 0.05, 420/1080 - 0.09], facecolor=C_CARD_BG)
    ax4.axis("off")
    
    plant_rows = [
        ("Factory Seiko", "Osaka, Japan", "9 Assets", "480 min", "99.88%", "$12,370", C_CORAL),
        ("Shenzhen Plant", "Shenzhen, China", "9 Assets", "420 min", "99.90%", "$13,983", C_AMBER),
        ("Factory Meiyo", "Tokyo, Japan", "9 Assets", "110 min", "99.97%", "$2,398", C_CYAN),
        ("Berlin Facility", "Berlin, Germany", "9 Assets", "20 min", "99.99%", "$1,041", C_EMERALD)
    ]
    ax4.text(0.02, 0.92, "PLANT NAME", color=C_TEXT_MUTED, fontsize=9, fontweight="bold")
    ax4.text(0.32, 0.92, "LOCATION", color=C_TEXT_MUTED, fontsize=9, fontweight="bold")
    ax4.text(0.55, 0.92, "DOWNTIME", color=C_TEXT_MUTED, fontsize=9, fontweight="bold")
    ax4.text(0.74, 0.92, "UPTIME", color=C_TEXT_MUTED, fontsize=9, fontweight="bold")
    ax4.text(0.88, 0.92, "LOSS ($)", color=C_TEXT_MUTED, fontsize=9, fontweight="bold")
    ax4.plot([0.02, 0.98], [0.86, 0.86], color=C_BORDER, linewidth=1)
    
    for idx, (pname, ploc, passets, pdow, pup, ploss, col) in enumerate(plant_rows):
        ypos = 0.72 - (idx * 0.19)
        # indicator dot
        ax4.scatter(0.02, ypos + 0.03, color=col, s=80)
        ax4.text(0.06, ypos + 0.01, pname, color=C_TEXT_LIGHT, fontsize=10, fontweight="bold")
        ax4.text(0.06, ypos - 0.05, passets, color=C_TEXT_MUTED, fontsize=8)
        ax4.text(0.32, ypos, ploc, color=C_TEXT_LIGHT, fontsize=9)
        ax4.text(0.55, ypos, pdow, color=col, fontsize=9.5, fontweight="bold")
        ax4.text(0.74, ypos, pup, color=C_TEXT_LIGHT, fontsize=9.5, fontweight="bold")
        ax4.text(0.88, ypos, ploss, color=C_TEXT_LIGHT, fontsize=9.5, fontweight="bold")
        if idx < 3: ax4.plot([0.02, 0.98], [ypos - 0.09, ypos - 0.09], color=C_BORDER, linewidth=0.5, linestyle=":")
        
    out_path = "reports/figures/powerbi_page_1_executive_overview.png"
    fig.savefig(out_path, facecolor=C_NAVY_BG, edgecolor="none")
    plt.close()
    print(f"Generated {out_path}")

# ==============================================================================
# PAGE 2: FACTORY PERFORMANCE
# ==============================================================================
def render_page_2():
    fig, ax_canvas = draw_powerbi_canvas("Page 2: Factory Performance", "Cross-Plant Reliability Benchmarking, Shift Variance & Sections", 1)
    
    # Row 1: KPI Cards (y=900, h=95)
    kpis = [
        (30, 900, 440, 95, "Benchmark Plant: Berlin", "99.9950 % Availability", "20 Mins Outage (Single Incident)", C_EMERALD),
        (490, 900, 440, 95, "Shift Vulnerability", "Morning Shift: 58.3%", "600 Mins Outage (Diurnal Shock)", C_CORAL),
        (950, 900, 440, 95, "Critical Facility Section", "Shenzhen Section 3", "410 Mins Downtime Concentrated", C_AMBER),
        (1410, 900, 480, 95, "Total Fleet Breakdown Incidents", "29 Distinct Episodes", "Shenzhen: 24 | Meiyo: 3 | Seiko: 1 | Berlin: 1", C_CYAN)
    ]
    for k in kpis:
        add_kpi_card(ax_canvas, *k)
        
    # Visual 1: Shift Downtime Distribution (Top-Left, x=30, y=470, w=910, h=410)
    add_visual_container(ax_canvas, 30, 470, 910, 410, "Operational Downtime by Shift (Morning vs Afternoon vs Night)")
    ax1 = fig.add_axes([30/1920 + 0.04, 470/1080 + 0.04, 910/1920 - 0.06, 410/1080 - 0.09], facecolor=C_CARD_BG)
    ax1.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax1.spines.values(): sp.set_color(C_BORDER)
    
    shifts = ["Shift 1 (Morning)\n06:00 - 14:00", "Shift 3 (Night)\n22:00 - 06:00", "Shift 2 (Afternoon)\n14:00 - 22:00"]
    s_mins = [600, 290, 140]
    bars = ax1.bar(shifts, s_mins, color=[C_CORAL, C_AMBER, C_CYAN], width=0.5, edgecolor=C_TEXT_LIGHT, linewidth=0.5)
    for b, val in zip(bars, s_mins):
        pct = (val / 1030) * 100
        ax1.text(b.get_x() + b.get_width()/2, val + 15, f"{val} min\n({val/60.0:.1f} hrs | {pct:.1f}%)", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=C_TEXT_LIGHT)
    ax1.set_ylim(0, 700)
    ax1.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax1.set_ylabel("Downtime (Minutes)", color=C_TEXT_MUTED, fontsize=9.5)
    
    # Visual 2: Section Breakdown (Top-Right, x=960, y=470, w=930, h=410)
    add_visual_container(ax_canvas, 960, 470, 930, 410, "Factory Section Vulnerability Heatmap (Shop-Floor Work Cell Mins)")
    ax2 = fig.add_axes([960/1920 + 0.06, 470/1080 + 0.04, 930/1920 - 0.09, 410/1080 - 0.09], facecolor=C_CARD_BG)
    
    # Matrix data:
    sec_matrix = np.array([
        [0, 0, 0, 20],      # Berlin (Sec 4)
        [70, 0, 40, 0],     # Meiyo (Sec 1: 70m, Sec 3: 40m)
        [0, 0, 0, 480],     # Seiko (Sec 4: 480m)
        [10, 0, 410, 0]     # Shenzhen (Sec 1: 10m, Sec 3: 410m)
    ])
    cax = ax2.imshow(sec_matrix, cmap="magma", aspect="auto", vmin=0, vmax=480)
    for i in range(4):
        for j in range(4):
            val = sec_matrix[i, j]
            ax2.text(j, i, f"{val} m" if val>0 else "-", ha="center", va="center", color=C_TEXT_LIGHT if val>50 else C_TEXT_MUTED, fontweight="bold", fontsize=10.5)
    ax2.set_xticks(range(4))
    ax2.set_xticklabels(["Section 1", "Section 2", "Section 3", "Section 4"], color=C_TEXT_LIGHT, fontsize=9.5)
    ax2.set_yticks(range(4))
    ax2.set_yticklabels(["Berlin Facility", "Factory Meiyo", "Factory Seiko", "Shenzhen Plant"], color=C_TEXT_LIGHT, fontsize=9.5)
    
    # Visual 3: Master Operations Scorecard Table (Bottom, x=30, y=30, w=1860, h=420)
    add_visual_container(ax_canvas, 30, 30, 1860, 420, "Global Manufacturing Operations Scorecard & Engineering Reliability Matrix")
    ax3 = fig.add_axes([30/1920 + 0.02, 30/1080 + 0.04, 1860/1920 - 0.04, 420/1080 - 0.09], facecolor=C_CARD_BG)
    ax3.axis("off")
    
    cols = ["FACTORY CODE", "FACILITY NAME", "LOCATION", "TELEMETRY CYCLES", "UNHEALTHY CYCLES", "TOTAL DOWNTIME", "AVAILABILITY %", "INCIDENTS", "MTBF (HRS)", "MTTR (MINS)", "OPERATING LOSS ($)", "STATUS"]
    col_x = [0.01, 0.11, 0.23, 0.33, 0.42, 0.50, 0.59, 0.67, 0.74, 0.81, 0.88, 0.95]
    for cx, ch in zip(col_x, cols):
        ax3.text(cx, 0.92, ch, color=C_TEXT_MUTED, fontsize=8.5, fontweight="bold", va="center")
    ax3.plot([0.01, 0.99], [0.85, 0.85], color=C_BORDER, linewidth=1.2)
    
    table_rows = [
        ("FAC-BER-03", "Berlin Facility", "Berlin, Germany", "40,176", "2", "20 min (0.33 hr)", "99.9950 %", "1", "6,695.7 hrs", "20.0 min", "$ 1,041.20", "Optimal", C_EMERALD),
        ("FAC-TYO-01", "Factory Meiyo", "Tokyo, Japan", "40,176", "11", "110 min (1.83 hr)", "99.9726 %", "3", "2,231.4 hrs", "36.7 min", "$ 2,398.20", "Good", C_CYAN),
        ("FAC-SZX-04", "Shenzhen Plant", "Shenzhen, China", "40,176", "42", "420 min (7.00 hr)", "99.8955 %", "24", "278.9 hrs", "17.5 min", "$ 13,983.10", "Chronic Risk", C_AMBER),
        ("FAC-OSA-02", "Factory Seiko", "Osaka, Japan", "40,176", "48", "480 min (8.00 hr)", "99.8805 %", "1", "6,688.0 hrs", "480.0 min", "$ 12,370.00", "Critical Risk", C_CORAL),
        ("FLEET TOTAL", "4 Global Facilities", "Global Network", "160,704", "103", "1,030 min (17.17 hr)", "99.9359 %", "29", "923.6 hrs", "35.5 min", "$ 29,792.50", "Enterprise", C_TEAL)
    ]
    for idx, (fcode, fname, floc, fcyc, funh, fdt, fav, finc, fmtbf, fmttr, floss, fstat, fcol) in enumerate(table_rows):
        ypos = 0.70 - (idx * 0.14)
        is_total = (idx == 4)
        fweight = "bold" if is_total else "normal"
        ax3.text(col_x[0], ypos, fcode, color=fcol, fontsize=9, fontweight="bold")
        ax3.text(col_x[1], ypos, fname, color=C_TEXT_LIGHT, fontsize=9, fontweight=fweight)
        ax3.text(col_x[2], ypos, floc, color=C_TEXT_MUTED, fontsize=8.5)
        ax3.text(col_x[3], ypos, fcyc, color=C_TEXT_LIGHT, fontsize=9)
        ax3.text(col_x[4], ypos, funh, color=fcol, fontsize=9, fontweight="bold")
        ax3.text(col_x[5], ypos, fdt, color=fcol, fontsize=9, fontweight="bold")
        ax3.text(col_x[6], ypos, fav, color=C_TEXT_LIGHT, fontsize=9, fontweight="bold")
        ax3.text(col_x[7], ypos, finc, color=C_TEXT_LIGHT, fontsize=9)
        ax3.text(col_x[8], ypos, fmtbf, color=C_TEXT_LIGHT, fontsize=9)
        ax3.text(col_x[9], ypos, fmttr, color=C_TEXT_LIGHT, fontsize=9)
        ax3.text(col_x[10], ypos, floss, color=fcol, fontsize=9, fontweight="bold")
        ax3.text(col_x[11], ypos, fstat, color=fcol, fontsize=9, fontweight="bold")
        ax3.plot([0.01, 0.99], [ypos - 0.05, ypos - 0.05], color=C_BORDER, linewidth=0.5 if not is_total else 1.2)
        
    out_path = "reports/figures/powerbi_page_2_factory_performance.png"
    fig.savefig(out_path, facecolor=C_NAVY_BG, edgecolor="none")
    plt.close()
    print(f"Generated {out_path}")

# ==============================================================================
# PAGE 3: MACHINE ANALYTICS & RELIABILITY
# ==============================================================================
def render_page_3():
    fig, ax_canvas = draw_powerbi_canvas("Page 3: Machine Analytics & Reliability", "Equipment Reliability Quadrants, Failure Severity & Incident Diagnostics", 2)
    
    # Row 1: KPI Cards (y=900, h=95)
    kpis = [
        (30, 900, 440, 95, "Fleet Reliability Index", "99.2 % Health Score", "Weighted Availability & MTTR", C_EMERALD),
        (490, 900, 440, 95, "Mean Time Between Failures", "923.6 Operating Hrs", "Fleet Operating Time / Incidents", C_CYAN),
        (950, 900, 440, 95, "Mean Time To Repair (MTTR)", "35.5 Minutes / Failure", "Ranging from 10m to 480m", C_AMBER),
        (1410, 900, 480, 95, "Chronic Bottleneck Asset", "LaserCutter (Shenzhen)", "23 Incidents | 430 Mins Outage", C_CORAL)
    ]
    for k in kpis:
        add_kpi_card(ax_canvas, *k)
        
    # Visual 1: Reliability Quadrant Scatter (Top-Left, x=30, y=470, w=910, h=410)
    add_visual_container(ax_canvas, 30, 470, 910, 410, "Reliability Matrix: MTBF (Reliability) vs MTTR (Maintainability)")
    ax1 = fig.add_axes([30/1920 + 0.045, 470/1080 + 0.04, 910/1920 - 0.07, 410/1080 - 0.09], facecolor=C_CARD_BG)
    ax1.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax1.spines.values(): sp.set_color(C_BORDER)
    
    # Points:
    pts = [
        ("LaserWelder", 480, 6688, C_CORAL, 400),
        ("LaserCutter", 18.7, 280, C_AMBER, 350),
        ("HeavyDutyDrill", 70, 2231, C_CYAN, 150),
        ("Furnace", 20, 6695, C_PURPLE, 100),
        ("CNC / Conveyor / Spot", 10, 6698, C_EMERALD, 80)
    ]
    for name, mttr, mtbf, col, sz in pts:
        ax1.scatter(mttr, mtbf, color=col, s=sz, alpha=0.9, edgecolors=C_TEXT_LIGHT, linewidths=1.2)
        ax1.text(mttr + 12, mtbf, name, color=C_TEXT_LIGHT, fontsize=9, fontweight="bold", va="center")
        
    ax1.axvline(60, color=C_BORDER, linestyle=":", linewidth=1.5)
    ax1.axhline(2000, color=C_BORDER, linestyle=":", linewidth=1.5)
    ax1.text(20, 6200, "QUADRANT I: Optimal\n(High MTBF, Low MTTR)", color=C_EMERALD, fontsize=8.5, fontweight="bold")
    ax1.text(280, 1000, "QUADRANT IV: Critical Hazard\n(Low MTBF, High MTTR)", color=C_CORAL, fontsize=8.5, fontweight="bold")
    ax1.set_xlabel("Mean Time To Repair - MTTR (Minutes)", color=C_TEXT_MUTED, fontsize=9.5)
    ax1.set_ylabel("Mean Time Between Failures - MTBF (Hours)", color=C_TEXT_MUTED, fontsize=9.5)
    ax1.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax1.set_xlim(0, 520)
    ax1.set_ylim(0, 7200)
    
    # Visual 2: Failure Incident Frequency Ranking (Top-Right, x=960, y=470, w=930, h=410)
    add_visual_container(ax_canvas, 960, 470, 930, 410, "Failure Incident Frequency by Equipment Type (Number of Breakdowns)")
    ax2 = fig.add_axes([960/1920 + 0.05, 470/1080 + 0.04, 930/1920 - 0.08, 410/1080 - 0.09], facecolor=C_CARD_BG)
    ax2.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax2.spines.values(): sp.set_color(C_BORDER)
    
    m_names = ["LaserCutter", "LaserWelder", "HeavyDutyDrill", "Furnace", "CNC", "ConveyorBelt", "SpotWelder", "AirWrench", "MetalPress"]
    m_inc = [23, 1, 1, 1, 1, 1, 1, 0, 0]
    bars = ax2.barh(m_names[::-1], m_inc[::-1], color=C_CYAN, height=0.6, edgecolor=C_TEAL)
    for b in bars:
        w = b.get_width()
        if w > 0:
            ax2.text(w + 0.5, b.get_y() + b.get_height()/2, f"{int(w)} Incident{'s' if w>1 else ''} ({w/29*100:.1f}%)", va="center", color=C_TEXT_LIGHT, fontsize=9, fontweight="bold")
        else:
            ax2.text(0.3, b.get_y() + b.get_height()/2, "0 (100% Reliability)", va="center", color=C_EMERALD, fontsize=8.5, fontstyle="italic")
    ax2.set_xlim(0, 26)
    ax2.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax2.set_xlabel("Number of Breakdown Incidents", color=C_TEXT_MUTED, fontsize=9.5)
    
    # Visual 3: Incident Log Table (Bottom, x=30, y=30, w=1860, h=420)
    add_visual_container(ax_canvas, 30, 30, 1860, 420, "Critical Equipment Failure Incident Diagnostic Log (Sample Outages)")
    ax3 = fig.add_axes([30/1920 + 0.02, 30/1080 + 0.04, 1860/1920 - 0.04, 420/1080 - 0.09], facecolor=C_CARD_BG)
    ax3.axis("off")
    
    log_cols = ["INCIDENT ID", "FACILITY", "EQUIPMENT", "SECTION", "DATE", "SHIFT", "OUTAGE (MINS)", "DURATION (HRS)", "SEVERITY CLASSIFICATION", "FINANCIAL LOSS ($)"]
    log_x = [0.01, 0.11, 0.23, 0.35, 0.44, 0.52, 0.62, 0.72, 0.81, 0.93]
    for cx, ch in zip(log_x, log_cols):
        ax3.text(cx, 0.92, ch, color=C_TEXT_MUTED, fontsize=8.5, fontweight="bold", va="center")
    ax3.plot([0.01, 0.99], [0.85, 0.85], color=C_BORDER, linewidth=1.2)
    
    sample_logs = [
        ("INC-026", "Factory Seiko", "LaserWelder", "Section 4", "2021-05-15", "Shift 1 (Morning)", "480 min", "8.00 hrs", "Catastrophic (> 4 hrs)", "$ 12,370.00", C_CORAL),
        ("INC-027", "Factory Meiyo", "HeavyDutyDrill", "Section 1", "2021-05-27", "Shift 3 (Night)", "70 min", "1.17 hrs", "Major Breakdown (1-4 hrs)", "$ 1,100.90", C_AMBER),
        ("INC-001", "Factory Meiyo", "LaserCutter", "Section 3", "2021-05-05", "Shift 3 (Night)", "30 min", "0.50 hrs", "Minor Interruption (< 1 hr)", "$ 720.00", C_CYAN),
        ("INC-028", "Berlin Facility", "Furnace", "Section 4", "2021-05-03", "Shift 2 (Afternoon)", "20 min", "0.33 hrs", "Minor Interruption (< 1 hr)", "$ 1,041.20", C_PURPLE),
        ("INC-005", "Shenzhen Plant", "LaserCutter", "Section 3", "2021-05-01", "Shift 3 (Night)", "30 min", "0.50 hrs", "Minor Interruption (< 1 hr)", "$ 607.50", C_CYAN),
        ("INC-015", "Shenzhen Plant", "LaserCutter", "Section 3", "2021-05-15", "Shift 1 (Morning)", "30 min", "0.50 hrs", "Minor Interruption (< 1 hr)", "$ 607.50", C_CYAN)
    ]
    for idx, (iid, ifac, idev, isec, idt, isht, imin, ihr, isev, iloss, icol) in enumerate(sample_logs):
        ypos = 0.72 - (idx * 0.12)
        ax3.text(log_x[0], ypos, iid, color=icol, fontsize=9, fontweight="bold")
        ax3.text(log_x[1], ypos, ifac, color=C_TEXT_LIGHT, fontsize=9)
        ax3.text(log_x[2], ypos, idev, color=C_TEXT_LIGHT, fontsize=9, fontweight="bold")
        ax3.text(log_x[3], ypos, isec, color=C_TEXT_MUTED, fontsize=8.5)
        ax3.text(log_x[4], ypos, idt, color=C_TEXT_LIGHT, fontsize=9)
        ax3.text(log_x[5], ypos, isht, color=C_TEXT_LIGHT, fontsize=8.5)
        ax3.text(log_x[6], ypos, imin, color=icol, fontsize=9, fontweight="bold")
        ax3.text(log_x[7], ypos, ihr, color=C_TEXT_LIGHT, fontsize=9)
        ax3.text(log_x[8], ypos, isev, color=icol, fontsize=9, fontweight="bold")
        ax3.text(log_x[9], ypos, iloss, color=C_TEXT_LIGHT, fontsize=9.5, fontweight="bold")
        ax3.plot([0.01, 0.99], [ypos - 0.04, ypos - 0.04], color=C_BORDER, linewidth=0.5)
        
    out_path = "reports/figures/powerbi_page_3_machine_analytics.png"
    fig.savefig(out_path, facecolor=C_NAVY_BG, edgecolor="none")
    plt.close()
    print(f"Generated {out_path}")

# ==============================================================================
# PAGE 4: FINANCIAL IMPACT & WHAT-IF RISK MODEL
# ==============================================================================
def render_page_4():
    fig, ax_canvas = draw_powerbi_canvas("Page 4: Financial Impact & Risk", "Cost Quantification, Scrap Exposure & Predictive ROI What-If Simulator", 3)
    
    # Row 1: KPI Cards (y=900, h=95)
    kpis = [
        (30, 900, 440, 95, "Total Monthly Outage Loss", "$ 29,792.50", "Across 4 Production Plants", C_CORAL),
        (490, 900, 440, 95, "Lost Production Throughput", "$ 18,450.50 (61.9%)", "Direct Finished Goods Loss", C_AMBER),
        (950, 900, 440, 95, "Scrap & WIP Spoilage Loss", "$ 7,400.00 (24.8%)", "Shenzhen Incurs $5,750 Scrap", C_CYAN),
        (1410, 900, 480, 95, "Annualized Net Value Captured", "$ 247,426.50 / yr", "Scenario C Target (395% ROI)", C_EMERALD)
    ]
    for k in kpis:
        add_kpi_card(ax_canvas, *k)
        
    # Visual 1: Financial Cost Components by Factory (Top-Left, x=30, y=470, w=910, h=410)
    add_visual_container(ax_canvas, 30, 470, 910, 410, "Factory Financial Exposure Breakdown by Cost Category ($ USD)")
    ax1 = fig.add_axes([30/1920 + 0.045, 470/1080 + 0.04, 910/1920 - 0.07, 410/1080 - 0.09], facecolor=C_CARD_BG)
    ax1.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax1.spines.values(): sp.set_color(C_BORDER)
    
    fac_labels = ["Shenzhen Plant", "Factory Seiko", "Factory Meiyo", "Berlin Facility"]
    p_loss = np.array([6591.5, 10000.0, 1397.0, 462.0])
    l_loss = np.array([1641.6, 1920.0, 301.2, 79.2])
    s_loss = np.array([5750.0, 450.0, 700.0, 500.0])
    
    b1 = ax1.bar(fac_labels, p_loss, label="Lost Production Throughput", color=C_CORAL, width=0.55)
    b2 = ax1.bar(fac_labels, l_loss, bottom=p_loss, label="Emergency Repair Labor", color=C_CYAN, width=0.55)
    b3 = ax1.bar(fac_labels, s_loss, bottom=p_loss + l_loss, label="WIP Scrap & Spoilage", color=C_AMBER, width=0.55)
    
    for i, (pl, ll, sl) in enumerate(zip(p_loss, l_loss, s_loss)):
        tot = pl + ll + sl
        ax1.text(i, tot + 300, f"${tot:,.0f}\n({tot/29792.5*100:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold", color=C_TEXT_LIGHT)
        
    ax1.set_ylim(0, 16000)
    ax1.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax1.set_ylabel("Financial Exposure ($ USD)", color=C_TEXT_MUTED, fontsize=9.5)
    ax1.legend(loc="upper right", framealpha=0.8, facecolor=C_NAVY_BG, edgecolor=C_BORDER, fontsize=8.5)
    
    # Visual 2: Machine Loss Treemap / Bar (Top-Right, x=960, y=470, w=930, h=410)
    add_visual_container(ax_canvas, 960, 470, 930, 410, "Equipment Financial Loss Attribution ($ USD & Share %)")
    ax2 = fig.add_axes([960/1920 + 0.05, 470/1080 + 0.04, 930/1920 - 0.08, 410/1080 - 0.09], facecolor=C_CARD_BG)
    ax2.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax2.spines.values(): sp.set_color(C_BORDER)
    
    devs = ["LaserCutter", "LaserWelder", "HeavyDutyDrill", "Furnace", "ConveyorBelt", "CNC", "SpotWelder"]
    d_loss = [14282.3, 12370.0, 1100.9, 1041.2, 377.8, 356.4, 263.9]
    colors_dev = [C_CORAL, C_AMBER, C_CYAN, C_PURPLE, C_TEAL, C_EMERALD, C_TEXT_MUTED]
    bars = ax2.barh(devs[::-1], d_loss[::-1], color=colors_dev[::-1], height=0.6, edgecolor=C_TEXT_LIGHT, linewidth=0.5)
    for b in bars:
        w = b.get_width()
        pct = (w / 29792.5) * 100
        ax2.text(w + 250, b.get_y() + b.get_height()/2, f"${w:,.0f} ({pct:.1f}%)", va="center", color=C_TEXT_LIGHT, fontsize=9, fontweight="bold")
    ax2.set_xlim(0, 17000)
    ax2.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax2.set_xlabel("Total Financial Loss ($ USD)", color=C_TEXT_MUTED, fontsize=9.5)
    
    # Visual 3: What-If Slicer & Live Simulator (Bottom-Left, x=30, y=30, w=800, h=420)
    add_visual_container(ax_canvas, 30, 30, 800, 420, "What-If Predictive Maintenance ROI Parameter Simulator")
    ax3 = fig.add_axes([30/1920 + 0.03, 30/1080 + 0.04, 800/1920 - 0.05, 420/1080 - 0.09], facecolor=C_CARD_BG)
    ax3.axis("off")
    
    ax3.text(0.04, 0.88, "INTERACTIVE WHAT-IF SLICER PARAMETER", color=C_TEXT_MUTED, fontsize=9.5, fontweight="bold")
    # Draw slider track
    slider_track = patches.Rectangle((0.04, 0.74), 0.90, 0.03, facecolor="#334155", edgecolor="none")
    slider_fill = patches.Rectangle((0.04, 0.74), 0.90 * 0.75, 0.03, facecolor=C_TEAL, edgecolor="none")
    slider_knob = patches.Circle((0.04 + (0.90 * 0.75), 0.755), 0.032, facecolor=C_TEXT_LIGHT, edgecolor=C_TEAL, linewidth=2)
    ax3.add_patch(slider_track)
    ax3.add_patch(slider_fill)
    ax3.add_patch(slider_knob)
    ax3.text(0.04, 0.64, "0%", color=C_TEXT_MUTED, fontsize=9)
    ax3.text(0.47, 0.64, "50%", color=C_TEXT_MUTED, fontsize=9)
    ax3.text(0.90, 0.64, "100%", color=C_TEXT_MUTED, fontsize=9)
    ax3.text(0.04 + (0.90 * 0.75), 0.82, "SELECTED: 75% DOWNTIME REDUCTION", color=C_TEAL, fontsize=9.5, fontweight="bold", ha="center")
    
    # Simulator output cards
    sim_cards = [
        (0.04, 0.34, 0.42, 0.22, "Monthly Net Savings", "$ 20,618.88", C_EMERALD),
        (0.52, 0.34, 0.42, 0.22, "Annual Net Savings", "$ 247,426.50", C_EMERALD),
        (0.04, 0.05, 0.42, 0.22, "Capital Payback", "2.4 Months", C_CYAN),
        (0.52, 0.05, 0.42, 0.22, "Year-1 Program ROI", "394.9 %", C_TEAL)
    ]
    for sx, sy, sw, sh, stitle, sval, scol in sim_cards:
        scard = patches.FancyBboxPatch((sx, sy), sw, sh, boxstyle="round,pad=0.02", facecolor="#131B30", edgecolor=scol, linewidth=1)
        ax3.add_patch(scard)
        ax3.text(sx + 0.03, sy + sh - 0.06, stitle.upper(), color=C_TEXT_MUTED, fontsize=8, fontweight="bold")
        ax3.text(sx + 0.03, sy + 0.05, sval, color=scol, fontsize=13, fontweight="bold")
        
    # Visual 4: Strategic Scenarios Comparison (Bottom-Right, x=860, y=30, w=1030, h=420)
    add_visual_container(ax_canvas, 860, 30, 1030, 420, "Strategic Scenario Payoff Comparison (Baseline vs Transformation)")
    ax4 = fig.add_axes([860/1920 + 0.04, 30/1080 + 0.04, 1030/1920 - 0.06, 420/1080 - 0.09], facecolor=C_CARD_BG)
    ax4.grid(color=C_GRID, linestyle="--", alpha=0.6)
    for sp in ax4.spines.values(): sp.set_color(C_BORDER)
    
    scenarios = ["Baseline (Reactive Status Quo)", "Scenario B (Fast-Swap Spares)", "Scenario A (Predictive Early Warning)", "Scenario C (Industry 4.0 Transformation)"]
    annual_loss = [357510.0, 268191.9, 174955.2, 110083.5]
    annual_savings = [0.0, 89318.1, 182554.8, 247426.5]
    
    y_pos = np.arange(len(scenarios))
    b1 = ax4.barh(y_pos, annual_loss, color=C_CORAL, height=0.55, label="Net Remaining Annual Loss ($)", alpha=0.85)
    b2 = ax4.barh(y_pos, annual_savings, left=annual_loss, color=C_EMERALD, height=0.55, label="Net Captured Annual Savings ($)", alpha=0.95)
    
    for i, (l_val, s_val) in enumerate(zip(annual_loss, annual_savings)):
        if s_val > 0:
            ax4.text(l_val + s_val + 6000, i, f"Saves ${s_val:,.0f} / yr", color=C_EMERALD, va="center", fontsize=9, fontweight="bold")
        else:
            ax4.text(l_val + 6000, i, f"Loss: ${l_val:,.0f} / yr", color=C_CORAL, va="center", fontsize=9, fontweight="bold")
            
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(scenarios, color=C_TEXT_LIGHT, fontsize=9.5)
    ax4.tick_params(colors=C_TEXT_LIGHT, labelsize=9)
    ax4.set_xlabel("Annualized Financial Exposure ($ USD)", color=C_TEXT_MUTED, fontsize=9.5)
    ax4.set_xlim(0, 430000)
    ax4.legend(loc="lower right", framealpha=0.8, facecolor=C_NAVY_BG, edgecolor=C_BORDER, fontsize=8.5)
    
    out_path = "reports/figures/powerbi_page_4_financial_risk.png"
    fig.savefig(out_path, facecolor=C_NAVY_BG, edgecolor="none")
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    print("Generating 4-Page Power BI PNG Dashboard Representation...")
    render_page_1()
    render_page_2()
    render_page_3()
    render_page_4()
    print("All 4 Power BI Dashboard PNG pages generated successfully.")

