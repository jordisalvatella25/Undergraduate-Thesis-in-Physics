# **T Cell Expansion On Activating Surface Simulation**

This directory contains the **TCellExpansionOnActivatingSurface** simulation, designed to study **T Cell proliferation via contact-dependent activation, growth and mitosis on an adhesive surface**.

## **Modelling decisions**

### **Contact plugin**

**Adhesion hierarchies** through defining adhesion constants. From strongest to weakest: TCell-Wall, TCell-Medium, TCell-TCell.

### **InitialConditionsSteppable**

Wall thickness.

Placement of T cells near the surface.

### **TCellActivationSteppable**

**Contact dependent activation**: cells activate upon interaction with the activating surface.

**Morphological changes after activation**: decreased lambdaVolume and lambdaSurface.

### **TCellGrowthSteppable**

Growth allowed only when:

- Volume < maximum growth volume.
- Pressure < maximum growth pressure.

**Different growth rates** for activated and non-activated cells.

### **TCellMitosisSteppable**

Division allowed only when:

- Volume > minimum division volume.
- Pressure < maximum division pressure.
- Accumulated divisions < maximum allowed divisions.
  
Maximum accumulated divisions set to 10.

**Cells are born already activated.**

Both child cells inherit **all parent attributes**, including **division history**.

## **Free parameters and trackers used in the simulation:**

| Steppable | Parameters | Trackers |
|----------|----------------------------|----------|
| **Contact Plugin** | Adhesion constants | — |
| **InitialConditionsSteppable** | wall_thickness<br>N_tcells<br>r_tcell<br>lambdaVolume<br>lambdaSurface| — |
| **TCellActivationSteppable** | lambdaVolume post‑activation<br>lambdaSurface post‑activation| Cells_counter.txt<br>(#TCells, #ActivatedTCells, %ActivatedTCells) |
| **TCellGrowthSteppable** | volume_threshold<br>pressure_threshold<br>base_growth_rate<br>growth_rate_multiplier | Mean_volume.txt<br>Mean_pressure.txt |
| **TCellMitosisSteppable** | volume_min_division<br>pressure_max_division<br>max_divisions | Total_divisions.txt |
| **EnergiesTrackerSteppable** | — | Volume_energy.txt<br>Surface_energy.txt<br>Adhesion_energy.txt<br>Total_energy.txt<br> |
| **WallContactTrackerSteppable** | — | Wall_contact_cells.txt<br>Wall_contact_area.txt |
| **DivisionStructureTrackerSteppable** | — | Initial_zero_divisions_tracker.txt<br>Division_histogram_tracker.txt |
| **VSRatioAndDistanceTrackerSteppable** | — | VS_Distance_tracker.txt<br>(VS_mean, D_mean) |

