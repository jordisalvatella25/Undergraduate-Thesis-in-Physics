from cc3d.core.PySteppables import *
import numpy as np

class MitosisSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        
        first_cell = self.new_cell(self.CONDENSING)
        self.cell_field[127:129, 127:129, 0] = first_cell
        
        first_cell.targetVolume = 25
        first_cell.lambdaVolume = 20.0
               

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """

        for cell in self.cell_list:
            cell.targetVolume += 0.2

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """

class CellDivisionSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list:
            if cell.volume>50:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self): # IT'S CALLED ONLY WHEN THERE IS A DIVISION
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0 #ONE OF THE CELLS IS STILL CONSIDERED THE SAME (THE PARENT CELL). WE UPDATE IT'S ATTRIBUTES           

        self.clone_parent_2_child()  # WE COPY TO THE CHILD CELL ALL PARENT'S ATTRIBUTES          

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        if self.parent_cell.type==1:
            self.child_cell.type=1


class FilesOutputSteppable(SteppableBasePy):
    def __init__(self, frequency=10):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        
        with open ("adhesion_energy.txt","w") as f:
            f.write("#MCS\tAdhesion_Energy\n")
        with open ("volume_energy.txt","w") as f:
            f.write("#MCS\tVolume_Energy\n")
        with open ("total_energy.txt","w") as f:
            f.write("#MCS\tTotal_Energy\n")
            
        with open ("cells_counter.txt","w") as f:
            f.write("#MCS\tCells_Number\n")
        with open ("mean_pressure.txt","w") as f:
            f.write("#MCS\tMean_Pressure\n")
        with open ("mean_volume.txt","w") as f:
            f.write("#MCS\tMean_Volume\n")
            
        self.J = {
            (1, 1): 10.0,
            (0, 1): 10.0, (1, 0): 10.0,
        }
        
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
        
        self.cells_plot = self.add_new_plot_window(
            title='Cells Number vs MCS',
            x_axis_title='MCS',
            y_axis_title='Cells Number',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True,
            config_options={'legend':True})
        self.cells_plot.add_plot("Cells Number", style='Lines', color='orange')

        self.pressure_plot = self.add_new_plot_window(title='Mean Pressure vs MCS',
            x_axis_title='MCS',
            y_axis_title='Mean Pressure',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True,
            config_options={'legend':True})
        self.pressure_plot.add_plot("Mean Pressure", style='Lines', color='purple')
        
        self.mean_volume_plot = self.add_new_plot_window(title='Mean Volume vs MCS',
            x_axis_title='MCS',
            y_axis_title='Mean Volume',
            x_scale_type='linear',
            y_scale_type='linear',
            grid=True,
            config_options={'legend':True})
        self.mean_volume_plot.add_plot("Mean Volume", style='Lines', color='blue')

    def step(self, mcs):
        
        Adhesion_Energy = 0.0
        for cell in self.cell_list: # Medium is not in self.cell_list
            for neigh, area in self.get_cell_neighbor_data_list(cell): 
                # get_cell_neighbor_data_list(cell) returns a list of tuplas (neighbor, area). Here, in the loop, we unpack the tupla into two variables
                if neigh is None: # If neighbour == None, the neighbour is the Medium
                    Adhesion_Energy += self.J[(cell.type, 0)] * area # Adhesion energy contribution from every cell in contact with the medium
                elif neigh.id > cell.id: # In order to only count one time the adhesion energy between a pair a of cells.
                    Adhesion_Energy += self.J[(cell.type, neigh.type)] * area
                    
        Volume_Energy = 0.0
        Pressure = 0.0
        Total_Volume = 0.0
        for cell in self.cell_list:
                lamb = cell.lambdaVolume
                V_target = cell.targetVolume
                V = cell.volume
                Volume_Energy += lamb*((V - V_target)**2)
                Pressure += (-2*lamb*(V-V_target))
                Total_Volume += V

        Mean_Pressure = Pressure/len(self.cell_list)
        Total_Energy = Adhesion_Energy + Volume_Energy
        Cells_number = len(self.cell_list)
        Mean_Volume = Total_Volume/len(self.cell_list)

        with open("adhesion_energy.txt", "a") as f:
            f.write(f"{mcs}\t{Adhesion_Energy}\n")
        with open("volume_energy.txt", "a") as f:
            f.write(f"{mcs}\t{Volume_Energy}\n")
        with open("total_energy.txt", "a") as f:
            f.write(f"{mcs}\t{Total_Energy}\n")
            
        with open("cells_counter.txt", "a") as f:
            f.write(f"{mcs}\t{Cells_number}\n")
        with open("mean_pressure.txt", "a") as f:
            f.write(f"{mcs}\t{Mean_Pressure}\n")
        with open("mean_volume.txt", "a") as f:
            f.write(f"{mcs}\t{Mean_Volume}\n")
        
        self.energy_plot.add_data_point("Total Energy", mcs, Total_Energy)
        self.energy_plot.add_data_point("Adhesion Energy", mcs, Adhesion_Energy)
        self.energy_plot.add_data_point("Volume Energy", mcs, Volume_Energy)
        
        self.cells_plot.add_data_point("Cells Number", mcs, Cells_number)
        
        self.pressure_plot.add_data_point("Mean Pressure", mcs, Mean_Pressure)
        self.mean_volume_plot.add_data_point("Mean Volume", mcs, Mean_Volume)
 


