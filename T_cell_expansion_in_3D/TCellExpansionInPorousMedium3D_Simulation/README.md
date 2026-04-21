# **T cell Expansion in Porous Medium Simulation**
## **OVERVIEW**

This directory contains the TCellExpansionInPorousMedium3D_Simulation, designed to study T cell proliferation via contact-dependent activation, growth and mitosis within a porous medium.

## **MODELLING DECISIONS**
#### **Contact plugin**
Adhesion hierarchies through defining adhesion constants. From strongest to weakest: TCell¬¬-Wall, TCell-Medium, TCell-TCell.
InitialConditionsSteppable
Spherical porous medium geometry.
Placement of T cells inside the porous structure.
Geometric relation between cell diameter and pore diameter.
TCellActivationSteppable
Contact dependent activation: cells activate upon interaction with the activating surface.
Morphological changes after activation: decreased lambdaVolume and lambdaSurface.
TCellGrowthSteppable
Growth allowed only when:
•	Volume < maximum growth volume.
•	Pressure < maximum growth pressure.
Different growth rates for activated and non-activated cells.
TCellMitosisSteppable
Division allowed only when:
•	Volume > minimum division volume.
•	Pressure < maximum division pressure.
•	Accumulated divisions < maximum allowed divisions.
Maximum accumulated divisions set to 10.
Cells are born already activated.
Both child cells inherit all parent attributes, including division history.
FREE PARAMETERS AND TRACKERS USED IN THE SIMULATION:
(Tabla)





| Steppable | Parameters | Trackers |
|----------|----------------------------|----------|
| **Contact Plugin** | Adhesion constants | — |
| **InitialConditionsSteppable** | R_porus<br>N_porus<br>N_tcells<br>r_tcell<br>lambdaVolume<br>lambdaSurface| — |
| **TCellActivationSteppable** | lambdaVolume post‑activation<br>lambdaSurface post‑activation| Cells_counter.txt<br>(#TCells, #ActivatedTCells, %ActivatedTCells) |
| **TCellGrowthSteppable** | volume_threshold<br>pressure_threshold<br>base_growth_rate<br>growth_rate_multiplier | Mean_volume.txt<br>Mean_pressure.txt |
| **TCellMitosisSteppable** | volume_min_division<br>pressure_max_division<br>max_divisions | Total_divisions.txt |
| **EnergiesTrackerSteppable** | — | Volume_energy.txt<br>Surface_energy.txt<br>Adhesion_energy.txt<br>Total_energy.txt<br> |
| **WallContactTrackerSteppable** | — | Wall_contact_cells.txt<br>Wall_contact_area.txt |
| **DivisionStructureTrackerSteppable** | — | Initial_zero_divisions_tracker.txt<br>Division_histogram_tracker.txt |
| **VSRatioAndDistanceTrackerSteppable** | — | VS_Distance_tracker.txt<br>(VS_mean, D_mean) |

