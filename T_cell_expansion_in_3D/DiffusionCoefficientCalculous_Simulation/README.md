Diffusion Coefficient Calculation of naïve T cells.
This directory contains the DiffusionCoefficientCalculous simulation (used to determine diffusion coefficient of the naïve T cells for the proliferation dynamics simulations) together with the data and results obtained from the different conducted computational replicas. In addition, the directory includes the post-simulation data-treatment script (Script_MSD_vs_lag_time_Plots_and_DiffusionCoefficient_Calculous), used to compute the Mean Square Displacement (hereafter MSD) and the diffusion coeffient, as well as to generate the corresponding plots.
All simulations were run for 250,000 MCS on a 100 × 100 × 100 lattice, allowing 20 cells with a radius of 2 voxels (the naïve T cells size in the simulations framework) to explore the lattice.
Taking into account that
•	the spatial units correspondence is 1.5 micrometers/voxel due to that naïve T cells have a real diameter of 6 micrometers, while in the simulations framework its diameter measures 4 voxels,
•	and that the diffusion coefficient has lenght$$^{2}$$/time dimensions,
comparing the simulated and theoretical diffusion coefficients yields the correspondence between simulation time (Monte Carlo Steps) and real time in in vitro T cell proliferation experiments.
For particles undergoing normal diffusion in a three dimensional system, the MSD grows linearly with time according to the relationship
$$\langle r^2(t) \rangle = 6 D\, t$$
MSD and D calculation procedure
In the DiffusionCoefficientCalculous simulation, the COM positions of each cell at every MCS are extracted through the UnwrappedCOMTrackerSteppable, which also unwraps the coordinates to correctly account for periodic boundary conditions. The simulation also includes a ShapeTrackerSteppable to monitor the mean volume/surface cells ratio.
To maximize statistical accuracy:
1.	For each lag time, the MSD is computed by averaging over all possible time origins (time origin averaging) within the same trajectory.
2.	The resulting MSD curves are then averaged over all cells (over all trajectories) for each lag time.
3.	The diffusion coefficient is obtained through a linear regression conducted over the MSD linear interval (the normal diffusion regime).
