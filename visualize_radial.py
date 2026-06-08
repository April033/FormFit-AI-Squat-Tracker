"""
FormFit Radial Session Visualization Tool - HQ 1080x1080 Edition
Forces non-GUI rendering to prevent silent Windows crashes.
Reads purely from real-time recorded session data.
"""
import os
import csv
import math
import numpy as np

# --- FORCE NON-GUI BACKEND ---
import matplotlib
matplotlib.use('Agg')  # Writes directly to disk, no window popup needed
import matplotlib.pyplot as plt

# Lock path to script's directory
csv_file = os.path.join(os.path.dirname(__file__), "session_data.csv")

# Ensure the session data exists (No more fake data generator!)
if not os.path.exists(csv_file):
    print(f"Error: {csv_file} not found. Please run main.py and record some squats first!")
    exit(1)

# --- READ AND PARSE THE DATA ---
reps = []
pace = []
angles = []

with open(csv_file, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        reps.append(int(row['rep_number']))
        pace.append(float(row['time_since_last_rep']))
        angles.append(int(row['knee_angle']))

total_reps = len(reps)

if total_reps == 0:
    print("Error: No repetitions found in the data file. Complete some reps first!")
    exit(1)

# --- CALCULATE METRICS (using real numbers) ---
avg_pace = sum(pace) / total_reps
slowest_rep = max(pace)
fastest_rep = min(pace)

mean_pace = avg_pace
std_dev = np.std(pace)
cv = std_dev / mean_pace if mean_pace > 0 else 0
consistency_score = max(0, min(100, int((1.0 - min(1.0, cv * 1.5)) * 100)))

# --- SCALING AND CAPPING VISUAL COORDINATES ---
# Cap visual pace at 10.0 seconds so standard reps spread out beautifully
plot_pace = [min(10.0, p) for p in pace]

# Map reps to radians
theta = [((r - 1) / total_reps) * 2 * np.pi for r in reps]
theta_closed = theta + [theta[0]]
plot_pace_closed = plot_pace + [plot_pace[0]]

# --- SET UP CANVAS (1080x1080 HQ Square) ---
fig, ax = plt.subplots(figsize=(10.8, 10.8), subplot_kw={'projection': 'polar'}, facecolor='black')
ax.set_facecolor('black')

# Position the plot to fill 90% of the entire 1080x1080 canvas
ax.set_position([0.05, 0.05, 0.9, 0.9])
ax.spines['polar'].set_visible(False)

# --- PLOT THE GLOWING NEON ORANGE LINE ---
ax.plot(theta_closed, plot_pace_closed, color='#FF5F1F', linewidth=24, alpha=0.03, zorder=2)
ax.plot(theta_closed, plot_pace_closed, color='#FF5F1F', linewidth=14, alpha=0.08, zorder=2)
ax.plot(theta_closed, plot_pace_closed, color='#FF5F1F', linewidth=7, alpha=0.18, zorder=2)
ax.plot(theta_closed, plot_pace_closed, color='#FF8C00', linewidth=2.0, alpha=1.0, zorder=3)

# --- SHADED REST & FATIGUE ARCS ---
for i in range(1, len(plot_pace)):
    if plot_pace[i] > 5.0:
        t_start = theta[i - 1]
        t_end = theta[i]
        t_grid = np.linspace(t_start, t_end, 10)
        ax.fill_between(t_grid, 0, plot_pace[i], color='#FF8C00', alpha=0.04, zorder=1)

# --- PLOT GRADIENT DATA POINTS ---
point_sizes = [((100 - angle) * 3) + 25 for angle in angles]
color_caps = [min(8.0, p) for p in pace]
scatter = ax.scatter(
    theta, 
    plot_pace, 
    c=color_caps, 
    cmap='RdYlGn_r', 
    s=point_sizes, 
    zorder=4, 
    edgecolors='#111111', 
    linewidths=0.5
)

# --- AXES AND GRID CONFIGURATION ---
ax.set_rgrids([2, 4, 6, 8, 10], labels=['2s', '4s', '6s', '8s', '10s+'], angle=0, color='white', fontsize=11, fontweight='bold')
ax.grid(True, color='#444444', linestyle='-', linewidth=1.2, zorder=0)

# Set grid limits
ax.set_ylim(0, 10.5)

# Rep numbers mapped around the outer ring
angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
labels = [f"Rep {int(d / 360 * total_reps)}" for d in angles_deg]
ax.set_thetagrids(angles_deg, labels, color='#AAAAAA', fontsize=11, fontweight='bold')

# Add spacing/padding
ax.tick_params(axis='x', pad=18)

# Rotate zero position to top center (North)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)  # Clockwise

# --- ANNOTATION LABELS (Only render if workout is long enough) ---
if total_reps > 220:
    rest_angle = (200 / total_reps) * 2 * np.pi
    ax.text(
        rest_angle, 10.2, "REST SPIKE", color='#39FF14', 
        fontsize=9.5, fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#001100', alpha=0.95, edgecolor='#39FF14', linewidth=1.2)
    )

if total_reps > 450:
    fatigue_angle = (430 / total_reps) * 2 * np.pi
    ax.text(
        fatigue_angle, 9.2, "FATIGUE ZONE", color='#FF3131', 
        fontsize=9.5, fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#110000', alpha=0.95, edgecolor='#FF3131', linewidth=1.2)
    )

# --- TITLE AT TOP ---
fig.text(
    0.5, 0.95, 
    "SESSION ANALYSIS — FORMFIT", 
    color='white', 
    fontsize=18, 
    fontweight='bold', 
    ha='center'
)

# --- STATS OVERLAY CARD (Bottom Left) ---
stats_text = (
    f"TOTAL REPS       : {total_reps}\n"
    f"AVG PACE         : {avg_pace:.2f}s\n"
    f"SLOWEST REP      : {slowest_rep:.2f}s\n"
    f"FASTEST REP      : {fastest_rep:.2f}s\n"
    f"CONSISTENCY SCORE: {consistency_score}%"
)

fig.text(
    0.06, 0.06,
    stats_text,
    color='white',
    fontsize=11,
    fontfamily='monospace',
    fontweight='bold',
    bbox=dict(boxstyle='round,pad=1.5', facecolor='#080808', alpha=0.95, edgecolor='#333333', linewidth=1.5)
)

# Save high-resolution 1080x1080 image directly to script's folder
output_image = os.path.join(os.path.dirname(__file__), "session_radial.png")
plt.savefig(
    output_image, 
    facecolor=fig.get_facecolor(), 
    edgecolor='none', 
    dpi=100,  # 10.8 inches * 100 dpi = 1080px
    bbox_inches='tight',
    pad_inches=0.1
)

print(f"✓ Success! HQ Radial visualization saved as '{output_image}'")