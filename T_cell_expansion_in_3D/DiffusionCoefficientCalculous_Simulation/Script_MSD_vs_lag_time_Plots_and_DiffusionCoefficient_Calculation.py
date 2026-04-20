## MSD vs lag time and Diffusion Coefficient calculation
"""

from google.colab import files
uploaded = files.upload()

import numpy as np
import matplotlib.pyplot as plt

max_mcs = None  # max mcs readed

# function output: trajectories[cell_id] = {"mcs": [...], "xu": [...], "yu": [...], "zu": [...]}

def read_trajectories(filename, max_mcs):

  trajectories = {}

  with open(filename, "r") as f:
    for line in f:
      if line.startswith("#"):
        continue

      parts = line.strip().split()
      mcs = int(parts[0])
      cell_id = int(parts[1])
      if max_mcs is not None and mcs > max_mcs:
        break
      xu = float(parts[5])
      yu = float(parts[6])
      zu = float(parts[7])

      if cell_id not in trajectories:
        trajectories[cell_id] = {
          "mcs": [],
          "xu": [],
          "yu": [],
          "zu": []
        }

      trajectories[cell_id]["mcs"].append(mcs)
      trajectories[cell_id]["xu"].append(xu)
      trajectories[cell_id]["yu"].append(yu)
      trajectories[cell_id]["zu"].append(zu)

  for cell_id in trajectories:
    trajectories[cell_id]["mcs"] = np.array(trajectories[cell_id]["mcs"], dtype=int)
    trajectories[cell_id]["xu"]  = np.array(trajectories[cell_id]["xu"], dtype=float)
    trajectories[cell_id]["yu"]  = np.array(trajectories[cell_id]["yu"], dtype=float)
    trajectories[cell_id]["zu"]  = np.array(trajectories[cell_id]["zu"], dtype=float)

  return trajectories

trajectories = read_trajectories("Unwrapped_COM_positions.txt", max_mcs)

cell_ids = sorted(list(trajectories.keys()))
print("Cells ids:", cell_ids)
print("Number of cells:", len(cell_ids))

all_mcs = set()
for cell_id in cell_ids:
    all_mcs.update(trajectories[cell_id]["mcs"])
all_mcs = np.array(sorted(all_mcs))
print("min MCS", np.min(all_mcs))
print("max MCS", np.max(all_mcs))
max_common_mcs = min(np.max(trajectories[cell_id]["mcs"]) for cell_id in trajectories)
print("max common_mcs", max_common_mcs)

# Function for MSD calculous. For each lag time:
  # 1) Mean over the trajectory for each cell
  # 2) Mean over all cells

# We use the unwrapped coordinates: xu, yu, zu

def MSD_calculous(trajectories):

    # we calculate delta_mcs
    sample_cell = list(trajectories.keys())[0] # we take the first cell to calculate delta_mcs
    sample_mcs = trajectories[sample_cell]["mcs"]
    delta_mcs = sample_mcs[1] - sample_mcs[0]

    # we calculate max_lag_index (lag_index = n = lag_time/delta_mcs)
    min_length = min(len(trajectories[cell_id]["mcs"]) for cell_id in trajectories)
    max_lag_index = min_length - 1

    lag_time_values = []
    msd_values = []

    # loop over all possible time lags
    for lag_index in range(1, max_lag_index + 1):

        lag_time = lag_index * delta_mcs
        msd_cells = []

        # loop over all cells
        for cell_id in trajectories:

            xu = trajectories[cell_id]["xu"]
            yu = trajectories[cell_id]["yu"]
            zu = trajectories[cell_id]["zu"]

            # squared displacement for the whole trajectory
            dx = xu[lag_index:] - xu[:-lag_index]
            dy = yu[lag_index:] - yu[:-lag_index]
            dz = zu[lag_index:] - zu[:-lag_index]

            sq_disp = dx**2 + dy**2 + dz**2

            # average over the trajectory for this cell
            msd_cell = np.mean(sq_disp)
            msd_cells.append(msd_cell)

        # average over cells and final addition to the time and MSD lists
        if len(msd_cells) > 0:
            msd_tau = np.mean(msd_cells)
            lag_time_values.append(lag_time)
            msd_values.append(msd_tau)

    return np.array(lag_time_values, dtype=float), np.array(msd_values, dtype=float)

# DATA EXTRACTION
lag_time, MSD = MSD_calculous(trajectories)

# FIRST MSD vs LAG TIME PLOT IN ORDER TO APPRECIATE THE LINEAR REGIME

plt.figure(figsize=(8,6))

plt.plot(lag_time, MSD, marker='o', markersize=0, linestyle='-', linewidth=0.5, color='red', label='MSD')

plt.xlabel('Lag time (MCS)', fontsize=16)
plt.ylabel('MSD', fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.savefig("MSD_vs_lag_time.png", dpi=300)

plt.show()

files.download("MSD_vs_lag_time.png")

# SELECT THE LINEAR REGIME

t_min = 0   # lineal regime min lag time
t_max = 200000  # lineal regime max lag time

# LINEAR REGIME ARRAYS

fit_times = []
fit_MSD = []

for i in range(len(lag_time)):
    if lag_time[i] >= t_min and lag_time[i] <= t_max:
        fit_times.append(lag_time[i])
        fit_MSD.append(MSD[i])

fit_times = np.array(fit_times)
fit_MSD = np.array(fit_MSD)

print("Number of points used in the linear regression:", len(fit_times))

# LINEAR REGRESION AND DIFUSSION COEFFICIENT CALCULOUS

coeffs, cov = np.polyfit(fit_times, fit_MSD, 1, cov=True)

slope = coeffs[0]
intercept = coeffs[1]

slope_std = np.sqrt(cov[0,0])
intercept_std = np.sqrt(cov[1,1])

D = slope / 6.0
D_std = slope_std / 6.0

R2 = np.corrcoef(fit_times, fit_MSD)[0,1]**2

print("LINEAR REGRESION RESULTS:")
print("---------------------------")
print(f"Slope = {slope:.6f} ± {slope_std:.6f}")
print(f"Intercept = {intercept:.6f} ± {intercept_std:.6f}")
print(f"Diffusion Coefficient = {D:.6f} ± {D_std:.6f}")
print(f"R^2 = {R2:.6f}")

# CALIBRATION LINE POINTS CALCULATION

fit_line = slope*fit_times + intercept

# FINAL PLOT

plt.figure(figsize=(8,6))

# MSD vs lag_time series
plt.plot(lag_time, MSD, marker='o', markersize=0, linestyle='-', linewidth=0.5, color='red', label='MSD')

# Linear regresion
plt.plot(fit_times, fit_line, linestyle='--', linewidth=2.5, color='black', label='Linear fit')

plt.xlabel('Lag time (MCS)', fontsize=16)
plt.ylabel('MSD', fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.savefig("MSD_vs_lag_time_with_linear_fit.png", dpi=300)

plt.show()

files.download("MSD_vs_lag_time_with_linear_fit.png")

import os

def delete(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f'{filename} correctly removed')
    else:
        print(f'{filename} not found')
    print('------------------------------')

delete("Unwrapped_COM_positions.txt")
