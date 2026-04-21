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

