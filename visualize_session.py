"""
FormFit Session Visualization Tool
Generates a minimal, high-contrast pace tracking line graph from session_data.csv
"""
import csv
import matplotlib.pyplot as plt
import os

# Lock path to script's folder
csv_file = os.path.join(os.path.dirname(__file__), "session_data.csv")

# Validate that the session data exists
if not os.path.exists(csv_file):
    print(f"Error: {csv_file} not found. Please complete a workout session first!")
    exit(1)

reps = []
pace = []

# Read parameters from the CSV file
with open(csv_file, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        reps.append(int(row['rep_number']))
        pace.append(float(row['time_since_last_rep']))

if not reps:
    print("Error: No repetitions found in the data file. Complete some reps first!")
    exit(1)

# Perform metrics calculations
total_reps = len(reps)
avg_pace = sum(pace) / total_reps
slowest_rep = max(pace)
fastest_rep = min(pace)

# Set up matplotlib dark theme canvas
fig, ax = plt.subplots(figsize=(10, 6), facecolor='black')
ax.set_facecolor('black')

# Plot the minimal orange fatigue curve line
ax.plot(
    reps, 
    pace, 
    color='#FF8C00',      # Dark Orange color
    linewidth=3, 
    marker='o', 
    markersize=8, 
    markerfacecolor='#FF8C00'
)

# Style borders and axes (Dark Gray and minimal)
ax.spines['bottom'].set_color('#333333')
ax.spines['left'].set_color('#333333')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Tick configurations
ax.tick_params(colors='white', which='both', labelsize=10)
ax.set_xlabel("Rep Number", color='#888888', fontsize=11, labelpad=12, fontweight='bold')
ax.set_ylabel("Time Since Last Rep (seconds)", color='#888888', fontsize=11, labelpad=12, fontweight='bold')
ax.set_title("SESSION PACE & FATIGUE TRACKER", color='white', fontsize=14, pad=20, fontweight='bold', loc='left')

# Format metrics overlay string
metrics_text = (
    f"TOTAL REPS : {total_reps}\n"
    f"AVG PACE   : {avg_pace:.2f}s\n"
    f"SLOWEST    : {slowest_rep:.2f}s\n"
    f"FASTEST    : {fastest_rep:.2f}s"
)

# Render the bold text overlay card inside the plot
ax.text(
    0.05, 0.95, 
    metrics_text,
    transform=ax.transAxes,
    color='white',
    fontsize=11,
    fontfamily='monospace',  # Consistent block spacing
    fontweight='bold',
    verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.8', facecolor='#111111', alpha=0.9, edgecolor='none')
)

# Clean rendering boundaries
plt.tight_layout()

# Save output to script's folder
output_image = os.path.join(os.path.dirname(__file__), "session_graph.png")
plt.savefig(output_image, facecolor=fig.get_facecolor(), edgecolor='none', dpi=150)
print(f"✓ Success! Session graph saved to disk as '{output_image}'")

# Display to screen
plt.show()