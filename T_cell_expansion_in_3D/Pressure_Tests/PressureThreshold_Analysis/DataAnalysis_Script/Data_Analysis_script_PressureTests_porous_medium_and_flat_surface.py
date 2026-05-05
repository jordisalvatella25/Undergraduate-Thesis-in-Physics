# Data Analysis Script for the Pressure Tests simulations *PressureTestInPorousMedium* and *PressureTestOnActivatingFlatSurface*

*   number_MCS
*   mcs_min_for_analysis

must be selected
"""

from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

import numpy as np
import matplotlib.pyplot as plt

# DEFINE DATA EXTRACTION FUNCTION

def read_file(filename):

    number_MCS = 90000
    columns = None

    with open(filename, "r") as f:

        for line in f:

            if line.startswith("#"):
                continue

            parts = line.strip().split()
            step = int(parts[0])

            if step > number_MCS:
                break

            if columns is None:
                ncols = len(parts)
                columns = [[] for _ in range(ncols)]

            for i in range(ncols):
                if i == 0:
                    value = int(parts[i])
                else:
                    value = float(parts[i])

                columns[i].append(value)

    columns = [np.array(col) for col in columns]

    return tuple(columns)

# DATA EXTRACTION

# PressurePercentilesTrackerSteppable

(
    mcs_PM,
    total_cells_PM,
    P_mean_PM,
    P10_PM,
    P20_PM,
    P30_PM,
    P40_PM,
    P50_PM,
    P60_PM,
    P70_PM,
    P75_PM,
    P80_PM,
    P90_PM,
    P95_PM,
    P99_PM,
    P_max_PM
) = read_file("Pressure_percentiles_PM.txt")

(
    mcs_FS,
    total_cells_FS,
    P_mean_FS,
    P10_FS,
    P20_FS,
    P30_FS,
    P40_FS,
    P50_FS,
    P60_FS,
    P70_FS,
    P75_FS,
    P80_FS,
    P90_FS,
    P95_FS,
    P99_FS,
    P_max_FS
) = read_file("Pressure_percentiles_FS.txt")

# TCellGrowthSteppable

mcs_pressure_PM, mean_pressure_PM, cells_over_threshold_PM = read_file("Mean_pressure_PM.txt")
mcs_pressure_FS, mean_pressure_FS, cells_over_threshold_FS = read_file("Mean_pressure_FS.txt")

# Select time window for analysis

mcs_min_for_analysis = 40000

mask_PM = mcs_PM >= mcs_min_for_analysis # mask_PM = [False, False, False, True, True, True, ...], is a boolean array of the same lenght as mcs_PM y values.
mask_FS = mcs_FS >= mcs_min_for_analysis

mask_pressure_PM = mcs_pressure_PM >= mcs_min_for_analysis
mask_pressure_FS = mcs_pressure_FS >= mcs_min_for_analysis

# Median calculation

percentile_names = ["P70", "P75", "P80", "P90", "P95", "P99"]

percentiles_PM = [P70_PM, P75_PM, P80_PM, P90_PM, P95_PM, P99_PM]
percentiles_FS = [P70_FS, P75_FS, P80_FS, P90_FS, P95_FS, P99_FS]

print("PRESSURE PERCENTILE MEDIANS")
print("--------------------------------")
print(f"Analysis window: MCS >= {mcs_min_for_analysis}")
print("")

print("Porous medium:")
for name, values in zip(percentile_names, percentiles_PM):
    median_value = np.median(values[mask_PM]) # values[mask_PM] means take only the values elements where mask_PM is true
    print(f"{name}_median_PM = {median_value:.4f}")

print("")
print("Flat surface:")
for name, values in zip(percentile_names, percentiles_FS):
    median_value = np.median(values[mask_FS])
    print(f"{name}_median_FS = {median_value:.4f}")

# Pressure thresholds calculation

print("Thresholds (conservative choice: minimum of both simulations):")

P90_common = min(np.median(P90_PM[mask_PM]), np.median(P90_FS[mask_FS]))
P95_common = min(np.median(P95_PM[mask_PM]), np.median(P95_FS[mask_FS]))

print(f"Common P90-based threshold ≈ {P90_common:.4f}")
print(f"Common P95-based threshold ≈ {P95_common:.4f}")

'''
print("Thresholds (medium choice):")
P90_common = (np.median(P90_PM[mask_PM]) + np.median(P90_FS[mask_FS])) / 2
P95_common = (np.median(P95_PM[mask_PM]) + np.median(P95_FS[mask_FS])) / 2

print(f"Common P90-based threshold ≈ {P90_common:.4f}")
print(f"Common P95-based threshold ≈ {P95_common:.4f}")
'''

# Max cells over pressure threshold and corresponing percentage calculation

mcs_pressure_PM_window = mcs_pressure_PM[mask_pressure_PM]
mcs_pressure_FS_window = mcs_pressure_FS[mask_pressure_FS]

cells_over_threshold_PM_window = cells_over_threshold_PM[mask_pressure_PM]
cells_over_threshold_FS_window = cells_over_threshold_FS[mask_pressure_FS]

total_cells_PM_window = total_cells_PM[mask_PM]
total_cells_FS_window = total_cells_FS[mask_FS]

idx_max_PM = np.argmax(cells_over_threshold_PM_window)
idx_max_FS = np.argmax(cells_over_threshold_FS_window)

max_cells_over_threshold_PM = cells_over_threshold_PM_window[idx_max_PM]
max_cells_over_threshold_FS = cells_over_threshold_FS_window[idx_max_FS]

total_cells_at_max_PM = total_cells_PM_window[idx_max_PM]
total_cells_at_max_FS = total_cells_FS_window[idx_max_FS]

max_percent_PM = (max_cells_over_threshold_PM/total_cells_at_max_PM)*100
max_percent_FS = (max_cells_over_threshold_FS/total_cells_at_max_FS)*100

print("")
print("CELLS OVER PRESSURE THRESHOLD")
print("--------------------------------")

print(f"PM: max cells over threshold = {int(max_cells_over_threshold_PM)} at MCS {int(mcs_pressure_PM_window[idx_max_PM])}")
print(f"PM: total cells at that MCS = {int(total_cells_at_max_PM)}")
print(f"PM: percentage = {max_percent_PM:.2f} %")

print("")

print(f"FS: max cells over threshold = {int(max_cells_over_threshold_FS)} at MCS {int(mcs_pressure_FS_window[idx_max_FS])}")
print(f"FS: total cells at that MCS = {int(total_cells_at_max_FS)}")
print(f"FS: percentage = {max_percent_FS:.2f} %")

# PLOT PRESSURE PERCENTILES VS MCS - PM

plt.figure(figsize=(8,6))

plt.plot(mcs_PM, P70_PM, linestyle='-', linewidth=0.5, color = 'orange', label='P70')
plt.plot(mcs_PM, P75_PM, linestyle='-', linewidth=0.5, color = 'purple', label='P75')
plt.plot(mcs_PM, P80_PM, linestyle='-', linewidth=0.5, color = 'brown', label='P80')
plt.plot(mcs_PM, P90_PM, linestyle='-', linewidth=0.5, color = 'red', label='P90')
plt.plot(mcs_PM, P95_PM, linestyle='-', linewidth=0.5, color = 'blue', label='P95')
plt.plot(mcs_PM, P99_PM, linestyle='-', linewidth=0.5, color = 'green', label='P99')

plt.axvline(
    x=mcs_min_for_analysis,
    linestyle='--',
    linewidth=1.5,
    color='black',
    label='Analysis window start'
)

plt.xlabel('MCS', fontsize=16)
plt.ylabel('Pressure', fontsize=16)

legend = plt.legend(fontsize=10, ncol=2)

for line in legend.get_lines():
    line.set_linewidth(2.0)

plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Pressure_percentiles_PM_vs_MCS.png", dpi=300)

plt.show()

files.download("Pressure_percentiles_PM_vs_MCS.png")

# PLOT PRESSURE PERCENTILES VS MCS - FS

plt.figure(figsize=(8,6))

plt.plot(mcs_FS, P70_FS, linestyle='-', linewidth=0.5, color = 'orange', label='P70')
plt.plot(mcs_FS, P75_FS, linestyle='-', linewidth=0.5, color = 'purple', label='P75')
plt.plot(mcs_FS, P80_FS, linestyle='-', linewidth=0.5, color = 'brown', label='P80')
plt.plot(mcs_FS, P90_FS, linestyle='-', linewidth=0.5, color = 'red', label='P90')
plt.plot(mcs_FS, P95_FS, linestyle='-', linewidth=0.5, color = 'blue', label='P95')
plt.plot(mcs_FS, P99_FS, linestyle='-', linewidth=0.5, color = 'green', label='P99')

plt.axvline(
    x=mcs_min_for_analysis,
    linestyle='--',
    linewidth=1.5,
    color='black',
    label='Analysis window start'
)

plt.xlabel('MCS', fontsize=16)
plt.ylabel('Pressure', fontsize=16)

legend = plt.legend(fontsize=10, ncol=2)

for line in legend.get_lines():
    line.set_linewidth(2.0)

plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Pressure_percentiles_FS_vs_MCS.png", dpi=300)

plt.show()

files.download("Pressure_percentiles_FS_vs_MCS.png")

# CROSSED PLOT P90 AND P95

plt.figure(figsize=(8,6))

plt.plot(mcs_PM, P90_PM, linestyle='-', linewidth=0.5, color='blue', label='P90 - PM')
plt.plot(mcs_PM, P95_PM, linestyle='-', linewidth=0.5, color='red', label='P95 - PM')

plt.plot(mcs_FS, P90_FS, linestyle='--', linewidth=0.5, color='green', label='P90 - FS')
plt.plot(mcs_FS, P95_FS, linestyle='--', linewidth=0.5, color='purple', label='P95 - FS')

plt.axvline(
    x=mcs_min_for_analysis,
    linestyle='--',
    linewidth=1.5,
    color='black',
    label='Analysis window start'
)

plt.xlabel('MCS', fontsize=16)
plt.ylabel('Pressure', fontsize=16)

legend = plt.legend(fontsize=10, ncol=2)

for line in legend.get_lines():
    line.set_linewidth(2.0)

plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Crossed_P90_P95_pressure_percentiles_vs_MCS.png", dpi=300)

plt.show()

files.download("Crossed_P90_P95_pressure_percentiles_vs_MCS.png")