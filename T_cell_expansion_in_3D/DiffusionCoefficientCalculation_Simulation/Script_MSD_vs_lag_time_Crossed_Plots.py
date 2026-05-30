## MSD vs lag time crossed plot for three replicas
"""

from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

from google.colab import files
uploaded = files.upload()

import numpy as np
import matplotlib.pyplot as plt

# EXTRACTION FUNCTION

def read_MSD_file(filename):
  lag_time = []
  MSD = []

  with open(filename, "r") as f:
    for line in f:
      if line.startswith("#"):
        continue
      else:
        parts = line.strip().split()
        lag_time.append(float(parts[0]))
        MSD.append(float(parts[1]))

  lag_time = np.array(lag_time)
  MSD = np.array(MSD)

  return lag_time, MSD

# DATA EXTRACTION

lag_time_1, MSD_1 = read_MSD_file("MSD_vs_lag_time_data_1.txt")
lag_time_2, MSD_2 = read_MSD_file("MSD_vs_lag_time_data_2.txt")
lag_time_3, MSD_3 = read_MSD_file("MSD_vs_lag_time_data_3.txt")

# FIRST MSD vs LAG TIME PLOT IN ORDER TO APPRECIATE THE LINEAR REGIME

plt.figure(figsize=(8,6))

plt.plot(lag_time_1, MSD_1, marker='o', markersize=0, linestyle='-', linewidth=1.0, color='red', label='Replica 1')
plt.plot(lag_time_2, MSD_2, marker='o', markersize=0, linestyle='-', linewidth=1.0, color='blue', label='Replica 2')
plt.plot(lag_time_3, MSD_3, marker='o', markersize=0, linestyle='-', linewidth=1.0, color='green', label='Replica 3')

plt.xlabel('Lag time (MCS)', fontsize=16)
plt.ylabel('MSD', fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.savefig("MSD_vs_lag_time_three_replicas.png", dpi=300)

plt.show()

files.download("MSD_vs_lag_time_three_replicas.png")

# SELECT THE LINEAR REGIME

t_min = 0        # lineal regime min lag time
t_max = 200000   # lineal regime max lag time

# LINEAR REGIME ARRAYS

fit_times_1 = []
fit_MSD_1 = []

for i in range(len(lag_time_1)):
    if lag_time_1[i] >= t_min and lag_time_1[i] <= t_max:
        fit_times_1.append(lag_time_1[i])
        fit_MSD_1.append(MSD_1[i])

fit_times_1 = np.array(fit_times_1)
fit_MSD_1 = np.array(fit_MSD_1)


fit_times_2 = []
fit_MSD_2 = []

for i in range(len(lag_time_2)):
    if lag_time_2[i] >= t_min and lag_time_2[i] <= t_max:
        fit_times_2.append(lag_time_2[i])
        fit_MSD_2.append(MSD_2[i])

fit_times_2 = np.array(fit_times_2)
fit_MSD_2 = np.array(fit_MSD_2)


fit_times_3 = []
fit_MSD_3 = []

for i in range(len(lag_time_3)):
    if lag_time_3[i] >= t_min and lag_time_3[i] <= t_max:
        fit_times_3.append(lag_time_3[i])
        fit_MSD_3.append(MSD_3[i])

fit_times_3 = np.array(fit_times_3)
fit_MSD_3 = np.array(fit_MSD_3)


print("Number of points used in the linear regression:")
print("---------------------------")
print("Replica 1:", len(fit_times_1))
print("Replica 2:", len(fit_times_2))
print("Replica 3:", len(fit_times_3))

# LINEAR REGRESSION AND DIFFUSION COEFFICIENT CALCULOUS

coeffs_1, cov_1 = np.polyfit(fit_times_1, fit_MSD_1, 1, cov=True)
slope_1 = coeffs_1[0]
intercept_1 = coeffs_1[1]
slope_std_1 = np.sqrt(cov_1[0,0])
intercept_std_1 = np.sqrt(cov_1[1,1])
D_1 = slope_1 / 6.0
D_std_1 = slope_std_1 / 6.0
R2_1 = np.corrcoef(fit_times_1, fit_MSD_1)[0,1]**2

coeffs_2, cov_2 = np.polyfit(fit_times_2, fit_MSD_2, 1, cov=True)
slope_2 = coeffs_2[0]
intercept_2 = coeffs_2[1]
slope_std_2 = np.sqrt(cov_2[0,0])
intercept_std_2 = np.sqrt(cov_2[1,1])
D_2 = slope_2 / 6.0
D_std_2 = slope_std_2 / 6.0
R2_2 = np.corrcoef(fit_times_2, fit_MSD_2)[0,1]**2

coeffs_3, cov_3 = np.polyfit(fit_times_3, fit_MSD_3, 1, cov=True)
slope_3 = coeffs_3[0]
intercept_3 = coeffs_3[1]
slope_std_3 = np.sqrt(cov_3[0,0])
intercept_std_3 = np.sqrt(cov_3[1,1])
D_3 = slope_3 / 6.0
D_std_3 = slope_std_3 / 6.0
R2_3 = np.corrcoef(fit_times_3, fit_MSD_3)[0,1]**2


print("LINEAR REGRESION RESULTS:")
print("---------------------------")

print("Replica 1:")
print(f"Slope = {slope_1:.10f} ± {slope_std_1:.10f}")
print(f"Intercept = {intercept_1:.10f} ± {intercept_std_1:.10f}")
print(f"Diffusion Coefficient = {D_1:.10f} ± {D_std_1:.10f}")
print(f"R^2 = {R2_1:.10f}")
print("---------------------------")

print("Replica 2:")
print(f"Slope = {slope_2:.10f} ± {slope_std_2:.10f}")
print(f"Intercept = {intercept_2:.10f} ± {intercept_std_2:.10f}")
print(f"Diffusion Coefficient = {D_2:.10f} ± {D_std_2:.10f}")
print(f"R^2 = {R2_2:.10f}")
print("---------------------------")

print("Replica 3:")
print(f"Slope = {slope_3:.10f} ± {slope_std_3:.10f}")
print(f"Intercept = {intercept_3:.10f} ± {intercept_std_3:.10f}")
print(f"Diffusion Coefficient = {D_3:.10f} ± {D_std_3:.10f}")
print(f"R^2 = {R2_3:.10f}")

# CALIBRATION LINE POINTS CALCULATION

fit_line_1 = slope_1*fit_times_1 + intercept_1
fit_line_2 = slope_2*fit_times_2 + intercept_2
fit_line_3 = slope_3*fit_times_3 + intercept_3

# FINAL PLOT

plt.figure(figsize=(8,6))

# MSD vs lag_time series
plt.plot(lag_time_1, MSD_1, marker='o', markersize=0, linestyle='-', linewidth=1.0, color='red', label=f'Replicate 1, linear fit (R²={R2_1:.3f})')
plt.plot(lag_time_2, MSD_2, marker='o', markersize=0, linestyle='-', linewidth=1.0, color='blue', label=f'Replicate 2, linear fit (R²={R2_2:.3f})')
plt.plot(lag_time_3, MSD_3, marker='o', markersize=0, linestyle='-', linewidth=1.0, color='green', label=f'Replicate 3, linear fit (R²={R2_3:.3f})')

# Linear regressions
plt.plot(fit_times_1, fit_line_1, linestyle='--', linewidth=1.0, color='black')
plt.plot(fit_times_2, fit_line_2, linestyle='--', linewidth=1.0, color='black')
plt.plot(fit_times_3, fit_line_3, linestyle='--', linewidth=1.0, color='black')

plt.xlabel('Lag time (MCS)', fontsize=18)
plt.ylabel('MSD', fontsize=18)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.savefig("MSD_vs_lag_time_three_replicas_with_linear_fit.png", dpi=300)

plt.show()

files.download("MSD_vs_lag_time_three_replicas_with_linear_fit.png")