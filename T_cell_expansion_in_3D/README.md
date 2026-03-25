#**Diffusion Tests of Spherical Cells**

This directory contains several simulation tests in order to explore how the **Brownian motion** of spherical cells and their **volume/surface relation** behave under different parameter configurations, allowing for finding a suitable range for these parameters.

In GGH framework, the effective diffusion coefficient of the cells depends on different factors:

- The **temperature** (T).
- The **adhesion constant between the cell and the medium** (J(cell,medium)).
- The **radius of the cell** (r)
- The **lambdaVolume** and **lambdaSurface** parameters.
  
In these tests, the parameters varied are lambdaVolume and lambdaSurface, while the rest are kept at fixed values:

- T=10,
- r=2.0 (corresponding to the targetVolume of a sphere of radius 2)
- J(cell,medium)=2.5.
  
All simulations were run for **200,000 MCS** on a **100 × 100 × 100 lattice**.
There are four test directories, each corresponding to a different pair of **(lambdaVolume, lambdaSurface)** values. Each directory contains the **tracked data** (**volume/surface ratio**, **accumulated traveled distance**, and **center of mass positions**) and the **corresponding plots**, including a **3D diagram showing the trajectory of the cells throughout the simulation**.
