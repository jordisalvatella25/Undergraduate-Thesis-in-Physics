# COMPARATIVE POST-DATA TREATMENT SCRIPT for *TCellExpansionInPorousMedium3D* and *TCellExpansionOnActivatingFlatSurface3D* simulations

### Used to make crossed plots
"""

from google.colab import files
uploaded = files.upload()

import numpy as np
import matplotlib.pyplot as plt

# DEFINE DATA EXTRACTION FUNCTION

def read_file(filename):

    number_MCS=150000
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

# TCellActivationSteppable
mcs_cells_PM, number_TotalCells_PM, number_TC_PM, number_ATC_PM, percentage_ATC_PM = read_file("Cells_counter_PM.txt")

mcs_cells_FS, number_TotalCells_FS, number_TC_FS, number_ATC_FS, percentage_ATC_FS = read_file("Cells_counter_FS.txt")

# TCellGrowthSteppable
mcs_mean_volume_PM, mean_volume_PM = read_file("Mean_volume_PM.txt")
mcs_mean_pressure_PM, mean_pressure_PM, cells_over_pressure_threshold_PM = read_file("Mean_pressure_PM.txt")

mcs_mean_volume_FS, mean_volume_FS = read_file("Mean_volume_FS.txt")
mcs_mean_pressure_FS, mean_pressure_FS, cells_over_pressure_threshold_FS = read_file("Mean_pressure_FS.txt")

# TCellMitosisSteppable
mcs_total_divisions_PM, total_divisions_PM = read_file("Total_divisions_PM.txt")

mcs_total_divisions_FS, total_divisions_FS = read_file("Total_divisions_FS.txt")

# EnergiesTrackerSteppable
mcs_adhesion_PM, energy_adhesion_PM = read_file("Adhesion_energy_PM.txt")
mcs_volume_PM, energy_volume_PM = read_file("Volume_energy_PM.txt")
mcs_surface_PM, energy_surface_PM = read_file("Surface_energy_PM.txt")
mcs_total_PM, energy_total_PM = read_file("Total_energy_PM.txt")

mcs_adhesion_FS, energy_adhesion_FS = read_file("Adhesion_energy_FS.txt")
mcs_volume_FS, energy_volume_FS = read_file("Volume_energy_FS.txt")
mcs_surface_FS, energy_surface_FS = read_file("Surface_energy_FS.txt")
mcs_total_FS, energy_total_FS = read_file("Total_energy_FS.txt")


# WallContactTrackerSteppable
mcs_contact_cells_PM, ATC_contact_cells_PM, TOTAL_contact_cells_PM, number_ATC_2_PM, percent_ATC_contact_cells_PM = read_file("Wall_contact_cells_PM.txt")
mcs_contact_area_PM, ATC_contact_area_PM, TOTAL_contact_area_PM = read_file("Wall_contact_area_PM.txt")

mcs_contact_cells_FS, ATC_contact_cells_FS, TOTAL_contact_cells_FS, number_ATC_2_FS, percent_ATC_contact_cells_FS = read_file("Wall_contact_cells_FS.txt")
mcs_contact_area_FS, ATC_contact_area_FS, TOTAL_contact_area_FS = read_file("Wall_contact_area_FS.txt")

# DivisionStructureTrackerSteppable
mcs_initial_proliferation_PM, initial_cells_PM, initial_cells_activated_PM, initial_cells_with_1ormore_divisions_PM, percent_initial_cells_with_1ormore_divisions_over_totalinitial_PM, percent_initial_cells_with_1ormore_divisions_over_activatedinitial_PM = read_file("Initial_cells_proliferation_tracker_PM.txt")
mcs_division_histogram_PM, total_cells_PM, Percent_div_0_PM, Percent_div_1_PM, Percent_div_2_PM, Percent_div_3_PM, Percent_div_4_PM, Percent_div_5_PM, Percent_div_6_PM, Percent_div_7_PM, Percent_div_8_PM, Percent_div_9_PM, Percent_div_10_PM = read_file("Division_histogram_tracker_PM.txt")

mcs_initial_proliferation_FS, initial_cells_FS, initial_cells_activated_FS, initial_cells_with_1ormore_divisions_FS, percent_initial_cells_with_1ormore_divisions_over_totalinitial_FS, percent_initial_cells_with_1ormore_divisions_over_activatedinitial_FS = read_file("Initial_cells_proliferation_tracker_FS.txt")
mcs_division_histogram_FS, total_cells_FS, Percent_div_0_FS, Percent_div_1_FS, Percent_div_2_FS, Percent_div_3_FS, Percent_div_4_FS, Percent_div_5_FS, Percent_div_6_FS, Percent_div_7_FS, Percent_div_8_FS, Percent_div_9_FS, Percent_div_10_FS = read_file("Division_histogram_tracker_FS.txt")

# VSRatioAndDistanceTrackerSteppable
mcs_VS_D_PM, VS_mean_PM, VS_ideal_mean_PM, Q_mean_PM, D_mean_PM = read_file("VS_Distance_tracker_PM.txt")
mcs_VS_D_FS, VS_mean_FS, VS_ideal_mean_FS, Q_mean_FS, D_mean_FS = read_file("VS_Distance_tracker_FS.txt")

# TCellActivationSteppable - PLOT NUMBER OF CELLS

plt.figure(figsize=(8,6))

plt.plot(mcs_cells_PM, number_TotalCells_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'black', label = 'Total - PM')
plt.plot(mcs_cells_PM, number_TC_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'blue', label = 'TC - PM')
plt.plot(mcs_cells_PM, number_ATC_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'red', label = 'ATC - PM')

plt.plot(mcs_cells_FS, number_TotalCells_FS, marker= 'o', markersize = 0, linestyle = '--', linewidth = 1.5, color = 'black', label = 'Total - FS')
plt.plot(mcs_cells_FS, number_TC_FS, marker= 'o', markersize = 0, linestyle = '--', linewidth = 1.5, color = 'blue', label = 'TC - FS')
plt.plot(mcs_cells_FS, number_ATC_FS, marker= 'o', markersize = 0, linestyle = '--', linewidth = 1.5, color = 'red', label = 'ATC - FS')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Number of cells',fontsize=16)
plt.legend(fontsize=10, ncol=2)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Crossed_Number_of_cells_vs_MCS.png", dpi=300)

plt.show()

files.download("Crossed_Number_of_cells_vs_MCS.png")

# TCellActivationSteppable - PLOT PERCENTAGE ACTIVATED CELLS

plt.figure(figsize=(8,6))

plt.plot(mcs_cells_PM, percentage_ATC_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'orange', label = 'Percentage ATC - PM')
plt.plot(mcs_cells_FS, percentage_ATC_FS, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'purple', label = 'Percentage ATC - FS')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Percentage ATC',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Crossed_Percentage_ATC_vs_MCS.png", dpi=300)

plt.show()

files.download("Crossed_Percentage_ATC_vs_MCS.png")

# WallContactTrackerSteppable - Percent of ATC touching Wall PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_contact_cells_PM, percent_ATC_contact_cells_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'orange', label = 'PM')
plt.plot(mcs_contact_cells_FS, percent_ATC_contact_cells_FS, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'purple', label = 'FS')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Percentage',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Crossed_Percent_ATC_touching_wall_vs_MCS.png", dpi=300)

plt.show()

files.download("Crossed_Percent_ATC_touching_wall_vs_MCS.png")

# DivisionStructureTrackerSteppable - Initial cells proliferation PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_initial_proliferation_PM, initial_cells_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'blue', label = 'Initial Cells')
plt.plot(mcs_initial_proliferation_PM, initial_cells_activated_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'red', label = 'Initial ATC - PM')
plt.plot(mcs_initial_proliferation_PM, initial_cells_with_1ormore_divisions_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'green', label=r'Initial cells with $\geq 1$ divisions - PM')

plt.plot(mcs_initial_proliferation_FS, initial_cells_activated_FS, marker= 'o', markersize = 0, linestyle = '--', linewidth = 1.5, color = 'red', label = 'Initial ATC - FS')
plt.plot(mcs_initial_proliferation_FS, initial_cells_with_1ormore_divisions_FS, marker= 'o', markersize = 0, linestyle = '--', linewidth = 1.5, color = 'green', label=r'Initial cells with $\geq 1$ divisions - FS')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Number of cells',fontsize=16)
plt.legend(fontsize=9, ncol=2)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Crossed_Initial_proliferation_vs_MCS.png", dpi=300)

plt.show()

files.download("Crossed_Initial_proliferation_vs_MCS.png")

# DivisionStructureTrackerSteppable - Percentage Initial cells proliferation over activated initial cells PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_initial_proliferation_PM, percent_initial_cells_with_1ormore_divisions_over_activatedinitial_PM, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'orange', label = 'PM')
plt.plot(mcs_initial_proliferation_FS, percent_initial_cells_with_1ormore_divisions_over_activatedinitial_FS, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'purple', label = 'FS')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Percentage',fontsize=16)
plt.legend(fontsize=8)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Crossed_Percent_Initial_cells_proliferation_over_activatedinitial_vs_MCS.png", dpi=300)

plt.show()

files.download("Crossed_Percent_Initial_cells_proliferation_over_activatedinitial_vs_MCS.png")