from cc3d.core.PySteppables import *
import numpy as np
import math
import random

class PorousMedia_SimulationSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):

        R_porus = 20
        N_porus = 30   
        pos_cent_x = np.random.randint(0,self.dim.x, size = N_porus)
        pos_cent_y = np.random.randint(0,self.dim.y, size = N_porus)
        pos_cent_z = np.random.randint(0,self.dim.z, size = N_porus)
        
        boolean_cavity = np.zeros((self.dim.x, self.dim.y, self.dim.z), dtype=bool)
        boolean_wall   = np.zeros((self.dim.x, self.dim.y, self.dim.z), dtype=bool)
        
        # we create the porous medium (the wall)
        
        wall = self.new_cell(self.WALL)
        
        for i,j,k in self.every_pixel():
            in_cavity = False
            for n in range(N_porus):
                if ((i-pos_cent_x[n])**2 + (j-pos_cent_y[n])**2+(k-pos_cent_z[n])**2)<(R_porus)**2:
                    boolean_cavity[i, j, k] = True
                    in_cavity = True                    
                    break
            if not(in_cavity):
                boolean_wall[i, j, k] = True
                self.cell_field[i,j,k] = wall
                
        # we create the T Cells as 'spheres'
        
        N_tcells = 100
        r_tcell = 2

        # offsets of the T Cell sphere
        sphere_offsets = []
        for i in range(-r_tcell, r_tcell+1):
            for j in range(-r_tcell, r_tcell+1):
                for k in range(-r_tcell, r_tcell+1):
                    if i*i + j*j + k*k <= r_tcell*r_tcell:
                        sphere_offsets.append((i, j, k))

        tcells_created = 0

        while tcells_created < N_tcells:

            # we choose a random voxel of the lattice
            
            x = np.random.randint(0, self.dim.x)
            y = np.random.randint(0, self.dim.y)
            z = np.random.randint(0, self.dim.z)

            # it must be inside a cavity
            if not boolean_cavity[x, y, z]:
                continue

            # we check if the cell voxels are valid
            valid = True
            for dx, dy, dz in sphere_offsets:
                xx = x + dx
                yy = y + dy
                zz = z + dz

                # out of the lattice --> invalid
                if not (0 <= xx < self.dim.x and 0 <= yy < self.dim.y and 0 <= zz < self.dim.z):
                    valid = False
                    break

                # invades the wall --> invalid
                if boolean_wall[xx, yy, zz]:
                    valid = False
                    break

                # invades other T cell --> invalid
                if self.cell_field[xx, yy, zz] is not None and self.cell_field[xx, yy, zz].type == self.TCELL:
                    valid = False
                    break

            if not valid:
                continue

            # if the voxels are valid, we create de T Cell
            tcell = self.new_cell(self.TCELL)

            for dx, dy, dz in sphere_offsets:
                xx = x + dx
                yy = y + dy
                zz = z + dz
                self.cell_field[xx, yy, zz] = tcell

            # adjust the volume and surface parameters
            tcell.targetVolume = (4/3)*math.pi*r_tcell*r_tcell*r_tcell
            tcell.lambdaVolume = 1.3
            tcell.targetSurface = 4*math.pi*r_tcell*r_tcell
            tcell.lambdaSurface = 1.3

            tcells_created += 1
            

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

class TCellActivationSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):

        # Create cell dictionaries and track activation
        for cell in self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL):
            '''if not hasattr(cell, 'dict') or cell.dict is None:
                cell.dict={}
            '''
            cell.dict['was_activated'] = cell.type == self.ACTIVATEDTCELL

        # Create a file to track number of TCells and ActivatedTCells
        self.counting_tracker_file = open(r"Cells_counter.txt", "w")
        self.counting_tracker_file.write("#MCS\tTCells_Number\tActivatedTCells_Number\tPercentage_ActivatedTCells\n")
        self.counting_tracker_file.flush()

        # Plot in real time the number of each type of T cell
        self.cells_counter_plot = self.add_new_plot_window(title='Cells number vs MCS',
            x_axis_title='MCS',
            y_axis_title='Cells number',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True,
            config_options={'legend':True})
        self.cells_counter_plot.add_plot("T Cells", style='Lines', color='green')
        self.cells_counter_plot.add_plot("Activated T Cells", style='Lines', color='red')

    def step(self, mcs):

        # Check regular T cells for new activations

        for cell in self.cell_list_by_type(self.TCELL):

            is_touching = self.is_touching_dynabead(cell)

            # If it is in contact with a Dynabead, activate it

            if is_touching:

                # Preserve cell properties when changing type

                #original_dict = dict(cell.dict) # (We create a copy of the dictionary)
                original_target_volume = cell.targetVolume
                original_target_surface = cell.targetSurface
                original_lambda_volume = cell.lambdaVolume
                original_lambda_surface = cell.lambdaSurface

                # Activate it

                cell.type = self.ACTIVATEDTCELL

                # Restore properties

                #cell.dict = original_dict
                cell.targetVolume = original_target_volume
                cell.targetSurface = original_target_surface
                cell.lambdaVolume = original_lambda_volume
                cell.lambdaSurface = original_lambda_surface

                # Update activation track

                cell.dict['was_activated'] = True

                # There is no code to deactivate cells: they remain activated

        # Record the number of TCells and ActivatedTCells
        TCells_number = len(self.cell_list_by_type(self.TCELL))
        ActivatedTCells_number = len(self.cell_list_by_type(self.ACTIVATEDTCELL))

        if mcs % 100 == 0:
            percent_activated = ((ActivatedTCells_number)/(TCells_number+ActivatedTCells_number))*100
            self.counting_tracker_file.write(f"{mcs}\t{TCells_number}\t{ActivatedTCells_number}\t{percent_activated}\n")
            self.counting_tracker_file.flush()

        self.cells_counter_plot.add_data_point("T Cells", mcs, TCells_number)
        self.cells_counter_plot.add_data_point("Activated T Cells", mcs, ActivatedTCells_number)

    def is_touching_dynabead(self, cell): # Definition of the TCell - Dynabead contact detector method
        for neighbor, area in self.get_cell_neighbor_data_list(cell):
            if neighbor and neighbor.type == self.WALL:
                return True
        return False

    def finish(self):

        self.counting_tracker_file.close()

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """


class CellGrowthSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):

        # Open the tracker output files
        self.mean_volume_tracker_file = open(r"Mean_volume.txt", "w")
        self.mean_volume_tracker_file.write("#MCS\tMean_volume\n")
        self.mean_volume_tracker_file.flush()

        self.mean_pressure_tracker_file = open(r"Mean_pressure.txt", "w")
        self.mean_pressure_tracker_file.write("#MCS\tMean_pressure\n")
        self.mean_pressure_tracker_file.flush()

        # Define the volume and pressure thresholds
        self.r_max = 5
        self.volume_threshold = (4/3)*math.pi*self.r_max*self.r_max*self.r_max
        self.pressure_threshold = 70

    def step(self, mcs):

        for cell in self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL):

            # Calculate the cell pressure
            cell.dict['pressure'] = -2*cell.lambdaVolume*(cell.volume-cell.targetVolume)

            # Check if the cell volume or the cell pressure exceed the threshold values
            if cell.volume >= self.volume_threshold or cell.dict['pressure'] >= self.pressure_threshold:
                continue

            # If the cell can grow, define growth rates for both types of T cells
            else:
                if cell.type == self.ACTIVATEDTCELL:
                    growth_rate = 0.001
                else:
                    growth_rate = 0.001

                # Update targetVolume (and targetSurface)
                cell.targetVolume += growth_rate
                cell.targetSurface = ((36*math.pi)**(1/3))*(cell.targetVolume**(2/3))

        # Register mean volume and mean pressure data in output files
        if mcs % 100 == 0:
            total_volume = 0.0
            total_pressure = 0.0
            all_Tcells_number = len(self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL))
            for cell in self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL):
                total_volume += cell.volume
                total_pressure += cell.dict['pressure']
            mean_volume = total_volume/all_Tcells_number
            mean_pressure = total_pressure/all_Tcells_number
            self.mean_volume_tracker_file.write(f"{mcs}\t{mean_volume}\n")
            self.mean_volume_tracker_file.flush()
            self.mean_pressure_tracker_file.write(f"{mcs}\t{mean_pressure}\n")
            self.mean_pressure_tracker_file.flush()

    def finish(self):

        self.mean_volume_tracker_file.close()
        self.mean_pressure_tracker_file.close()

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """


class TCellMitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def start(self):

        # Define the minimum volume, the maximum pressure and the maximum number of divisions for mitosis
        self.r_min_division = 4
        self.volume_min_division = (4/3)*math.pi*self.r_min_division*self.r_min_division*self.r_min_division
        self.pressure_max_division = 70
        self.max_divisions = 10

        # Initialize division counter for all T Cells
        for cell in self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL):
            cell.dict['division_count'] = 0

        # Create a total divisions counter
        self.total_divisions_counter = 0

        # Open the total divisions counter output file
        self.total_divisions_tracker_file = open(r"Total_divisions.txt", "w")
        self.total_divisions_tracker_file.write("#MCS\tTotal_divisions\n")
        self.total_divisions_tracker_file.flush()

        # Plot in real time the number total divisions
        self.divisions_counter_plot = self.add_new_plot_window(title='Total divisions vs MCS',
            x_axis_title='MCS',
            y_axis_title='Total divisions',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True,
            config_options={'legend':True})
        self.divisions_counter_plot.add_plot("Total divisions", style='Lines', color='blue')

    def step(self, mcs):

        # Select the T cells that reunite the conditions to divide
        cells_to_divide=[]
        for cell in self.cell_list_by_type(self.ACTIVATEDTCELL):
            if cell.volume >= self.volume_min_division and cell.dict['pressure'] < self.pressure_max_division and cell.dict['division_count'] < self.max_divisions:
                cells_to_divide.append(cell)

        # Divide them
        for cell in cells_to_divide:
            self.divide_cell_random_orientation(cell)
            self.total_divisions_counter += 1

        # Register total divisions
        if mcs % 100 == 0:
            self.total_divisions_tracker_file.write(f"{mcs}\t{self.total_divisions_counter}\n")
            self.total_divisions_tracker_file.flush()

        self.divisions_counter_plot.add_data_point("Total divisions", mcs, self.total_divisions_counter)

    def update_attributes(self):

        # Reduce the parent targetVolume, update properly its targetSurface and increment its division count
        self.parent_cell.targetVolume /= 2.0
        self.parent_cell.targetSurface = ((36*math.pi)**(1/3))*(self.parent_cell.targetVolume**(2/3))
        self.parent_cell.dict['division_count'] += 1

        # Clone parent cell attributes to child cell including division history
        self.clone_parent_2_child() # The child cell is born already activated

        # Set the child division counter to 0
        self.child_cell.dict['division_count'] = 0

    def finish(self):

        self.total_divisions_tracker_file.close()


class EnergiesTrackerSteppable(SteppableBasePy):
    def __init__(self, frequency=10):
        SteppableBasePy.__init__(self, frequency)

    def start(self):

        # Open the output data files
        self.volume_energy_file = open(r"Volume_energy.txt", "w")
        self.volume_energy_file.write("#MCS\tVolume_energy\n")
        self.volume_energy_file.flush()
        '''
        self.adhesion_energy_file = open(r"Adhesion_energy.txt", "w")
        self.adhesion_energy_file.write("#MCS\tAdhesion_energy\n")
        self.adhesion_energy_file.flush()
        '''
        self.total_energy_file = open(r"Total_energy.txt", "w")
        self.total_energy_file.write("#MCS\tTotal_energy\n")
        self.total_energy_file.flush()

        # Create the data plots
        '''
        self.energy_plot = self.add_new_plot_window(title='Energies vs MCS',
            x_axis_title='MCS',
            y_axis_title='Energy',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True,
            config_options={'legend':True})
        self.energy_plot.add_plot("Total Energy", style='Lines', color='green')
        self.energy_plot.add_plot("Adhesion Energy", style='Lines', color='red')
        self.energy_plot.add_plot("Volume Energy", style='Lines', color='blue')
        '''

    def step(self, mcs):
                    
        # Calculate the energy values
        Adhesion_energy = 0.0

        Volume_energy = 0.0
        for cell in self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL):
                Volume_energy += cell.lambdaVolume*((cell.volume - cell.targetVolume)**2)

        Total_energy = Adhesion_energy + Volume_energy
        
        if mcs % 100 == 0:
            # Register the data
            self.volume_energy_file.write(f"{mcs}\t{Volume_energy}\n")
            self.volume_energy_file.flush()
            '''
            self.adhesion_energy_file.write(f"{mcs}\t{Adhesion_energy}\n")
            self.adhesion_energy_file.flush()
            '''
            self.total_energy_file.write(f"{mcs}\t{Total_energy}\n")
            self.total_energy_file.flush()

        # Plot the data
        '''
        self.energy_plot.add_data_point("Total Energy", mcs, Total_energy)
        self.energy_plot.add_data_point("Adhesion Energy", mcs, Adhesion_energy)
        self.energy_plot.add_data_point("Volume Energy", mcs, Volume_energy)
        '''
        
    def finish(self):

        self.volume_energy_file.close()
        '''
        self.adhesion_energy_file.close()
        '''
        self.total_energy_file.close()
        
class COM_and_VS_TrackerSteppable(SteppableBasePy):

    def __init__(self, frequency=10):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        self.COM_and_VS_file = open(r"COM_and_VS_tracker.txt", "w")
        self.COM_and_VS_file.write("#MCS\tMean_displacement\tMean_VS_ratio\n")
        self.COM_and_VS_file.flush()

        for cell in self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL):
            cell.dict['initial_COM'] = (cell.xCOM, cell.yCOM, cell.zCOM)

    def step(self, mcs):
        total_disp = 0.0
        total_vs = 0.0
        count = 0

        for cell in self.cell_list_by_type(self.TCELL, self.ACTIVATEDTCELL):
            x0, y0, z0 = cell.dict['initial_COM']
            dx = cell.xCOM - x0
            dy = cell.yCOM - y0
            dz = cell.zCOM - z0
            disp = math.sqrt(dx*dx + dy*dy + dz*dz)
            total_disp += disp
            V = cell.volume
            S = cell.surface
            if S > 0:
                total_vs += V / S
            count += 1

        mean_disp = total_disp / count if count > 0 else 0.0
        mean_vs = total_vs / count if count > 0 else 0.0

        self.COM_and_VS_file.write(f"{mcs}\t{mean_disp}\t{mean_vs}\n")
        self.COM_and_VS_file.flush()

    def finish(self):
        self.COM_and_VS_file.close()
