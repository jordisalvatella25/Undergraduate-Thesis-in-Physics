# POST-DATA TREATMENT SCRIPT for *TCellExpansionInPorousMedium3D* and *TCellExpansionOnActivatingFlatSurface3D* simulations
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
mcs_cells, number_TotalCells, number_TC, number_ATC, percentage_ATC = read_file("Cells_counter.txt")

# TCellGrowthSteppable
mcs_mean_volume, mean_volume = read_file("Mean_volume.txt")
mcs_mean_pressure, mean_pressure = read_file("Mean_pressure.txt")

# TCellMitosisSteppable
mcs_total_divisions, total_divisions = read_file("Total_divisions.txt")

# EnergiesTrackerSteppable
mcs_adhesion, energy_adhesion = read_file("Adhesion_energy.txt")
mcs_volume, energy_volume = read_file("Volume_energy.txt")
mcs_surface, energy_surface = read_file("Surface_energy.txt")
mcs_total, energy_total = read_file("Total_energy.txt")

# WallContactTrackerSteppable
mcs_contact_cells, ATC_contact_cells, TOTAL_contact_cells, number_ATC_2, percent_ATC_contact_cells = read_file("Wall_contact_cells.txt")
mcs_contact_area, ATC_contact_area, TOTAL_contact_area = read_file("Wall_contact_area.txt")

# DivisionStructureTrackerSteppable
mcs_initial_proliferation, initial_cells, initial_cells_activated, initial_cells_with_1ormore_divisions, percent_initial_cells_with_1ormore_divisions_over_totalinitial, percent_initial_cells_with_1ormore_divisions_over_activatedinitial = read_file("Initial_cells_proliferation_tracker.txt")
mcs_division_histogram, total_cells, Percent_div_0, Percent_div_1, Percent_div_2, Percent_div_3, Percent_div_4, Percent_div_5, Percent_div_6, Percent_div_7, Percent_div_8, Percent_div_9, Percent_div_10 = read_file("Division_histogram_tracker.txt")

# VSRatioAndDistanceTrackerSteppable
mcs_VS_D, VS_mean, VS_ideal_mean, Q_mean, D_mean = read_file("VS_Distance_tracker.txt")

'''
plt.figure(figsize=(13,6))
plt.plot(mcs_total, energy_total, marker= 'o', markersize = 0, linestyle = '-', linewidth = 0.5, color = 'green', label = 'Total Energy')
plt.axhline(y=mean_total_energy, color = 'red', linestyle = '-', linewidth = 1.5, label = f'Mean Energy = {mean_total_energy:.0f}')
plt.xlabel('MCS')
plt.ylabel('Total Energy')
plt.legend()
plt.grid(True)

plt.savefig("Total_Energy_vs_MCS.png", dpi=300)

plt.show()

files.download("Total_Energy_vs_MCS.png")
'''

# TCellActivationSteppable - PLOT NUMBER OF CELLS

plt.figure(figsize=(8,6))

plt.plot(mcs_cells, number_TotalCells, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'black', label = 'Total cells')
plt.plot(mcs_cells, number_TC, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'blue', label = 'T cells')
plt.plot(mcs_cells, number_ATC, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'red', label = 'Activated T cells')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Number of cells',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Number_of_cells_vs_MCS.png", dpi=300)

plt.show()

files.download("Number_of_cells_vs_MCS.png")

# TCellActivationSteppable - PLOT PERCENTAGE ACTIVATED CELLS

plt.figure(figsize=(8,6))

plt.plot(mcs_cells, percentage_ATC, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'black', label = 'Percentage Activated T cells')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Percentage ATC',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Percentage_ATC_vs_MCS.png", dpi=300)

plt.show()

files.download("Percentage_ATC_vs_MCS.png")

# TCellGrowthSteppable - MEAN VOLUME PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_mean_volume, mean_volume, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'navy', label = 'Mean Volume')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Mean Volume',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Mean_volume_vs_MCS.png", dpi=300)

plt.show()

files.download("Mean_volume_vs_MCS.png")

# TCellGrowthSteppable - MEAN PRESSURE PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_mean_pressure, mean_pressure, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'darkviolet', label = 'Mean Pressure')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Mean Pressure',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Mean_pressure_vs_MCS.png", dpi=300)

plt.show()

files.download("Mean_pressure_vs_MCS.png")

# TCellMitosisSteppable - PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_total_divisions, total_divisions, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'darkblue', label = 'Total Divisions')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Total divisions',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Total_divisions_vs_MCS.png", dpi=300)

plt.show()

files.download("Total_divisions_vs_MCS.png")

# EnergiesTrackerSteppable - PLOT

plt.figure(figsize=(8,6))


plt.plot(mcs_adhesion, energy_adhesion, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'red', label = 'Adhesion Energy')
plt.plot(mcs_volume, energy_volume, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'blue', label = 'Volume Energy')
plt.plot(mcs_surface, energy_surface, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'orange', label = 'Surface Energy')
plt.plot(mcs_total, energy_total, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'green', label = 'Total Energy')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Energy',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Energies_vs_MCS.png", dpi=300)

plt.show()

files.download("Energies_vs_MCS.png")

# WallContactTrackerSteppable - Number of ATC touching Wall PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_contact_cells, ATC_contact_cells, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'black', label = 'ATC touching Wall')
plt.plot(mcs_contact_cells, number_ATC_2, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'red', label = 'ATC')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Number of cells',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("ATC_touching_wall_vs_MCS.png", dpi=300)

plt.show()

files.download("ATC_touching_wall_vs_MCS.png")

# WallContactTrackerSteppable - Percent of ATC touching Wall PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_contact_cells, percent_ATC_contact_cells, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'darkblue', label = 'Percent of ATC touching Wall')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Percentage',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Percent_ATC_touching_wall_vs_MCS.png", dpi=300)

plt.show()

files.download("Percent_ATC_touching_wall_vs_MCS.png")

# WallContactTrackerSteppable - Wall contact area PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_contact_area, ATC_contact_area, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'red', label = 'ATC-Wall contact area')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Contact area',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Contact_area_vs_MCS.png", dpi=300)

plt.show()

files.download("Contact_area_vs_MCS.png")

# DivisionStructureTrackerSteppable - Initial cells proliferation PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_initial_proliferation, initial_cells, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'blue', label = 'Initial cells')
plt.plot(mcs_initial_proliferation, initial_cells_activated, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'red', label = 'Initial cells Activated')
plt.plot(mcs_initial_proliferation, initial_cells_with_1ormore_divisions, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'green', label=r'Initial cells with $\geq 1$ divisions')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Number of cells',fontsize=16)
plt.legend(fontsize=10)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Initial_proliferation_vs_MCS.png", dpi=300)

plt.show()

files.download("Initial_proliferation_vs_MCS.png")

# DivisionStructureTrackerSteppable - Percentage Initial cells proliferation over activated initial cells PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_initial_proliferation, percent_initial_cells_with_1ormore_divisions_over_activatedinitial, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'green', label = r'Initial ATC with $\geq 1$ division (%)')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Percentage',fontsize=16)
plt.legend(fontsize=8)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Percent_Initial_cells_proliferation_over_activatedinitial_vs_MCS.png", dpi=300)

plt.show()

files.download("Percent_Initial_cells_proliferation_over_activatedinitial_vs_MCS.png")

# DivisionStructureTrackerSteppable - Division histogram PLOT

plt.figure(figsize=(10,6))

plt.stackplot(
    mcs_division_histogram,
    Percent_div_0,
    Percent_div_1,
    Percent_div_2,
    Percent_div_3,
    Percent_div_4,
    Percent_div_5,
    Percent_div_6,
    Percent_div_7,
    Percent_div_8,
    Percent_div_9,
    Percent_div_10,
    labels=[
        '0 divisions',
        '1 division',
        '2 divisions',
        '3 divisions',
        '4 divisions',
        '5 divisions',
        '6 divisions',
        '7 divisions',
        '8 divisions',
        '9 divisions',
        '10 divisions'
    ]
)

plt.xlabel('MCS', fontsize=16)
plt.ylabel('Population percentage', fontsize=16)

plt.xlim(np.min(mcs_division_histogram), np.max(mcs_division_histogram))
plt.ylim(0,100)

plt.legend(loc='lower left', fontsize=10, ncol=2)

plt.grid(True)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Division_histogram_vs_MCS.png", dpi=300)

plt.show()

files.download("Division_histogram_vs_MCS.png")

# VSRatioAndDistanceTrackerSteppable - Q_mean PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_VS_D, Q_mean, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'green', label = 'Q')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Q',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("Q_mean_vs_MCS.png", dpi=300)

plt.show()

files.download("Q_mean_vs_MCS.png")

# VSRatioAndDistanceTrackerSteppable - D_mean PLOT

plt.figure(figsize=(8,6))

plt.plot(mcs_VS_D, D_mean, marker= 'o', markersize = 0, linestyle = '-', linewidth = 2, color = 'green', label = 'Mean Distance Traveled')

plt.xlabel('MCS',fontsize=16)
plt.ylabel('Mean Distance',fontsize=16)
plt.legend(fontsize=14)
plt.grid(True)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.savefig("D_mean_vs_MCS.png", dpi=300)

plt.show()

files.download("D_mean_vs_MCS.png")