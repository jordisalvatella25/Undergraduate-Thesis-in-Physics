| Steppable | Parameters | Trackers |
|----------|----------------------------|----------|
| **Contact Plugin** | Adhesion constants | — |
| **InitialConditionsSteppable** | R_porus<br>N_porus<br>N_tcells<br>r_tcell<br>lambdaVolume<br>lambdaSurface| — |
| **TCellActivationSteppable** | lambdaVolume post‑activation (fixed)<br>lambdaSurface post‑activation (fixed) | Cells_counter.txt<br>(#TCells, #ActivatedTCells, %ActivatedTCells)<br>freq = 100 (plots freq = 1) |
| **TCellGrowthSteppable** | volume_threshold<br>pressure_threshold<br>base_growth_rate<br>growth_rate_multiplier | Mean_volume.txt (freq = 100)<br>Mean_pressure.txt (freq = 100) |
| **TCellMitosisSteppable** | volume_min_division<br>pressure_max_division<br>max_divisions (fixed) | Total_divisions.txt<br>freq = 100 (plots freq = 1) |
| **EnergiesTrackerSteppable** | — | Volume_energy.txt (freq = 100)<br>Surface_energy.txt (freq = 100)<br>Adhesion_energy.txt (freq = 100)<br>Total_energy.txt (freq = 100)<br>(plots freq = 100) |
| **WallContactTrackerSteppable** | — | Wall_contact_cells.txt (freq = 100)<br>Wall_contact_area.txt (freq = 100) |
| **DivisionStructureTrackerSteppable** | — | Initial_zero_divisions_tracker.txt (freq = 100)<br>Division_histogram_tracker.txt (freq = 100) |
| **VSRatioAndDistanceTrackerSteppable** | — | VS_Distance_tracker.txt<br>(VS_mean, D_mean)<br>freq = 100 |
| **HeightMonitoringSteppable** *(only in Activating Surface simulation)* | z_warning (fixed)<br>z_top (fixed) | Height_monitoring.txt (freq = 100) |
