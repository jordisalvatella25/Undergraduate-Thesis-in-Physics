# **Diffusion Coefficient Calculation of naïve T cells**

This directory contains the **DiffusionCoefficientCalculation** simulation (used to determine the **diffusion coefficient of the naïve T cells for the proliferation dynamics simulations**) together with the data and results obtained from the different computational replicas conducted. In addition, the directory includes the post-simulation data-treatment script (**Script_MSD_vs_lag_time_Plots_and_DiffusionCoefficient_Calculation**), used to compute the Mean Square Displacement (hereafter MSD) and the diffusion coefficient, as well as to generate the corresponding plots.

All simulations were run for **250,000 MCS** on a **100 × 100 × 100 lattice**, allowing **20** cells with a radius of **2** voxels (the naïve T cell size in the simulations framework) to explore the lattice.

Taking into account that
- the **spatial-units correspondence is 1.5 micrometers/voxel** due to that naïve T cells have a real diameter of 6 micrometers, while in the simulations framework its diameter measures 4 voxels,
- and that the diffusion coefficient has lenght $$^{2}$$ /time dimensions,

comparing the **simulated** and **theoretical** diffusion coefficients allow to determine the  correspondence between simulation time (Monte Carlo Steps) and real time of *in vitro* T cell proliferation experiments.

For particles undergoing **normal diffusion** in a **three-dimensional** system, the MSD grows linearly with time according to the relationship MSD $$(t)=6Dt$$.

## **MSD $$(t)$$ and $$D$$ calculation procedure**

In the **DiffusionCoefficientCalculation** simulation, the COM positions of each cell at every MCS are extracted through the **UnwrappedCOMTrackerSteppable**, which also unwraps the coordinates to correctly account for **periodic boundary conditions**. The simulation also includes a **ShapeTrackerSteppable** to monitor the mean volume/surface cells ratio.

To maximize statistical accuracy:
1.	For each lag time, the MSD is computed by averaging **over all possible time origins** (time origin averaging) **within the same trajectory**.
2.	The resulting MSD curves are then **averaged over all cells (over all trajectories)** for each lag time.
3.	The diffusion coefficient is obtained through a **linear regression** conducted **over the MSD linear interval (the normal diffusion regime)**.
