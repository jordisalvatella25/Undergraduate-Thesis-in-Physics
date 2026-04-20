from cc3d.core.PySteppables import *
import numpy as np
import math

class InitialConditionsSteppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        
        # we create the T Cells as 'spheres'

        N_tcells = 20
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
            
            # we check if the cell voxels are valid
            
            valid = True
            for dx, dy, dz in sphere_offsets:
                xx = x + dx
                yy = y + dy
                zz = z + dz

                if not (0 <= xx < self.dim.x and 0 <= yy < self.dim.y and 0 <= zz < self.dim.z):
                    valid = False
                    break

                if self.cell_field[xx, yy, zz] is not None:
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
            tcell.lambdaVolume = 1.2
            tcell.targetSurface = 4*math.pi*r_tcell*r_tcell
            tcell.lambdaSurface = 1.5

            tcells_created += 1

    def step(self, mcs):
        pass

    def finish(self):
        pass

    def on_stop(self):
        pass
      

class UnwrappedCOMTrackerSteppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):

        # open output file
        self.file = open("Unwrapped_COM_positions.txt", "w")
        self.file.write("#MCS\tcell_id\tx\ty\tz\txu\tyu\tzu\n")
        self.file.flush()

        # we create dictionaries to store previous wrapped COM and current unwrapped COM
        self.prev_COM = {}
        self.unwrapped_COM = {}

        # get lattice dimensions (for periodic conditions correction)
        self.Dx = self.dim.x
        self.Dy = self.dim.y
        self.Dz = self.dim.z

        # we initialize the dictionaries and write initial positions
        for cell in self.cell_list_by_type(self.TCELL):
            x = cell.xCOM
            y = cell.yCOM
            z = cell.zCOM

            self.prev_COM[cell.id] = (x, y, z)
            self.unwrapped_COM[cell.id] = (x, y, z)

            self.file.write(f"0\t{cell.id}\t{x}\t{y}\t{z}\t{x}\t{y}\t{z}\n")

        self.file.flush()

    def step(self, mcs):

        for cell in self.cell_list_by_type(self.TCELL):

            x_prev, y_prev, z_prev = self.prev_COM[cell.id]
            xu_prev, yu_prev, zu_prev = self.unwrapped_COM[cell.id]

            x = cell.xCOM
            y = cell.yCOM
            z = cell.zCOM

            # wrapped displacement
            dx = x - x_prev
            dy = y - y_prev
            dz = z - z_prev

            # we correct the calculus because of the periodic conditions
            dx -= self.Dx*round(dx/self.Dx)
            dy -= self.Dy*round(dy/self.Dy)
            dz -= self.Dz*round(dz/self.Dz)

            # we update unwrapped coordinates
            xu = xu_prev + dx
            yu = yu_prev + dy
            zu = zu_prev + dz

            # we store updated positions
            self.prev_COM[cell.id] = (x, y, z)
            self.unwrapped_COM[cell.id] = (xu, yu, zu)

            # we update the output file
            self.file.write(f"{mcs}\t{cell.id}\t{x}\t{y}\t{z}\t{xu}\t{yu}\t{zu}\n")
        
        self.file.flush()

    def finish(self):
        if not self.file.closed:
            self.file.close()

    def on_stop(self):
        if not self.file.closed:
            self.file.close()
            
            
class ShapeTrackerSteppable(SteppableBasePy):

    def __init__(self, frequency=100):
        SteppableBasePy.__init__(self, frequency)

    def start(self):

        self.VS_mean_file = open("VS_mean_tracker.txt", "w")
        self.VS_mean_file.write("#MCS\tVS_mean\n")
        self.VS_mean_file.flush()

    def step(self, mcs):

        vs_list = []

        for cell in self.cell_list_by_type(self.TCELL):
            V = cell.volume
            S = cell.surface
            VS = V / S if S > 0 else 0.0
            vs_list.append(VS)

        if len(vs_list) > 0:
            VS_mean = sum(vs_list) / len(vs_list)
            self.VS_mean_file.write(f"{mcs}\t{VS_mean}\n")
            self.VS_mean_file.flush()

    def finish(self):
        self.VS_mean_file.close()