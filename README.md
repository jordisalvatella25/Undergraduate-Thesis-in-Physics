# **Three-dimensional modelling of cell expansion using a generalized spin model - Undergraduate Thesis in Physics**

This repository contains the computational work developed for my Bachelor's Thesis, which addresses the development of three-dimensional computational simulations to model immune cell proliferation dynamics within material environments using CompuCell3D, an open-source Glazier-Graner-Hogeweg (GGH) modelling framework.

The GGH model is based on a generalized spin model typical of statistical physics applied to complex systems. It uses the Monte-Carlo method and a stochastic modified Metropolis algorithm, which allows for the kinetic evolution of the system. It allows the study of many biological and biomedical processes through the computational simulation of cell behaviors and interactions using an intuitive mathematical formalism. The Hamiltonian of the system and its terms and parameters are defined. These parameters can be static or dynamic. In addition, many extensions can be added to the model in order to reproduce more and better biological behaviors, such as adding terms in the Hamiltonian, external fields or off-lattice extensions. CompuCell3D, as an open-source GGH modeling framework, provides many facilities for this method implementation.

The goals are:
- Explore the GGH model by building and analyzing standard models provided in the official CompuCell3D documentation, as well as several variations of them to deepen understanding.
- Develop a three-dimensional simulation to model cell contact dependent growth and division within a material and study its behaviour under different parameter configurations.

## **Repository structure**

The repository is organized into two main directories:

1)	Exploring_the_GGH_Model

This directory contains a collection of exploratory simulations (and their results) used to explore and become familiar with the model and CompuCell3D software.


2)	T_cell_expansion_in_3D

This directory contains the three-dimensional simulations to model cell contact dependent growth and division within a material.

It includes:

	T Cell Expansion in Porous Medium simulation.
	T Cell Expansion on Activating Flat Surface.
	Diffusion Coefficient calculation simulation.
	Diffusion Test simulation.
	Several preliminary simulations used in the developing process of the final 3D expansion models.

TCellExpansionInPorousMedium3D and TCellExpansionOnActivatingSurface simulations are used to compare how environmental structure affects T cell proliferation dynamics.

