from cc3d.core.PySteppables import *
import numpy as np

class Inverted_Cell_SortingSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """

class EnergyOutputSteppable(SteppableBasePy):
    def __init__(self, frequency=10):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        self.J = {
            (1, 1): 2.0,
            (2, 2): 16.0,
            (1, 2): 11.0, (2, 1): 11.0,
            (0, 1): 6.0, (1, 0): 6.0,
            (0, 2): 16.0, (2, 0): 16.0,
        }
        self.volume_params = {
            1: {"lambda": 2.0, "target": 25},
            2: {"lambda": 2.0, "target": 25},
        }
        with open("adhesion_energy.txt", "w") as f:
            f.write("#MCS\tAdhesionEnergy\n")
        with open("volume_energy.txt", "w") as f:
            f.write("#MCS\tVolumeEnergy\n")
        with open("total_energy.txt", "w") as f:
            f.write("#MCS\tTotalEnergy\n")


    def step(self, mcs):
        Adhesion_Energy = 0.0
        for cell in self.cell_list: # Medium is not in self.cell_list
            for neigh, area in self.get_cell_neighbor_data_list(cell):
                if neigh is None: # If neighbour == None, the neighbour is the Medium
                    Adhesion_Energy += self.J[(cell.type, 0)] * area # Adhesion energy contribution from every cell in contact with the medium
                elif neigh.id > cell.id: # In order to only count one time the adhesion energy between a pair a of cells.
                    Adhesion_Energy += self.J[(cell.type, neigh.type)] * area
        
        
        Volume_Energy = 0.0
        for cell in self.cell_list:
            if cell.type in self.volume_params:
                lamb = self.volume_params[cell.type]["lambda"]
                V_target = self.volume_params[cell.type]["target"]
                V = cell.volume
                Volume_Energy += lamb*((V - V_target)**2)

        Total_Energy = Adhesion_Energy + Volume_Energy

        with open("adhesion_energy.txt", "a") as f:
            f.write(f"{mcs}\t{Adhesion_Energy}\n")
        with open("volume_energy.txt", "a") as f:
            f.write(f"{mcs}\t{Volume_Energy}\n")
        with open("total_energy.txt", "a") as f:
            f.write(f"{mcs}\t{Total_Energy}\n")
