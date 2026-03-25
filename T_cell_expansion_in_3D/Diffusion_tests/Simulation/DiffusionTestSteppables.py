from cc3d.core.PySteppables import *
import numpy as np
import math

class DiffusionTestSteppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        
        # we create the T Cells as 'spheres'

        N_tcells = 3
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
            tcell.lambdaVolume = 1.5
            tcell.targetSurface = 4*math.pi*r_tcell*r_tcell
            tcell.lambdaSurface = 2

            tcells_created += 1

    def step(self, mcs):
        pass

    def finish(self):
        pass

    def on_stop(self):
        pass


class DiffusionTrackerSteppable(SteppableBasePy):

    def __init__(self, frequency=10):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        
        # we create the output file for the V/S relation and distance traveled data
        self.tracker_file = open("Diffusion_tracker.txt", "w")
        self.tracker_file.write("#MCS\tVS_1\tVS_2\tVS_3\tVS_mean\tD1\tD2\tD3\tD_mean\n")
        self.tracker_file.flush()

        # we create diccionaries to store the previous COM and the traveled distance for each cell
        self.prev_COM = {}
        self.D = {}

        for cell in self.cell_list_by_type(self.TCELL):
            self.prev_COM[cell.id] = (cell.xCOM, cell.yCOM, cell.zCOM)
            self.D[cell.id] = 0.0

        self.Dx = self.dim.x
        self.Dy = self.dim.y
        self.Dz = self.dim.z

    def step(self, mcs):
        
        # we arrange the cells by id
        cells = list(self.cell_list_by_type(self.TCELL))
        cells = sorted(cells, key=lambda c: c.id)

        VS_list = [] # V/S relation for each cell
        D_list = [] # Total traveled distance for each cell

        for cell in cells:
            V = cell.volume
            S = cell.surface
            VS = V / S if S > 0 else 0.0
            VS_list.append(VS)

            x_prev, y_prev, z_prev = self.prev_COM[cell.id]

            dx = cell.xCOM - x_prev
            dy = cell.yCOM - y_prev
            dz = cell.zCOM - z_prev
            
            # we correct the calculus because of the periodic conditions
            dx -= self.Dx * round(dx / self.Dx)
            dy -= self.Dy * round(dy / self.Dy)
            dz -= self.Dz * round(dz / self.Dz)

            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            self.D[cell.id] += dist

            self.prev_COM[cell.id] = (cell.xCOM, cell.yCOM, cell.zCOM)

            D_list.append(self.D[cell.id])

        if len(VS_list) == 3:
            VS_mean = sum(VS_list) / 3.0
            D_mean = sum(D_list) / 3.0
            self.tracker_file.write(
                f"{mcs}\t"
                f"{VS_list[0]}\t{VS_list[1]}\t{VS_list[2]}\t{VS_mean}\t"
                f"{D_list[0]}\t{D_list[1]}\t{D_list[2]}\t{D_mean}\n"
            )
            self.tracker_file.flush()

    def finish(self):
        self.tracker_file.close()


class COM_TrackerSteppable(SteppableBasePy):

    def __init__(self, frequency=10):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        
        # we create the output file for COM positions
        self.file = open("COM_positions.txt", "w")
        self.file.write("#MCS\tx1\ty1\tz1\tx2\ty2\tz2\tx3\ty3\tz3\n")
        self.file.flush()

    def step(self, mcs):
        cells = list(self.cell_list_by_type(self.TCELL))
        cells = sorted(cells, key=lambda c: c.id)

        if len(cells) == 3:
            c1, c2, c3 = cells
            self.file.write(
                f"{mcs}\t"
                f"{c1.xCOM}\t{c1.yCOM}\t{c1.zCOM}\t"
                f"{c2.xCOM}\t{c2.yCOM}\t{c2.zCOM}\t"
                f"{c3.xCOM}\t{c3.yCOM}\t{c3.zCOM}\n"
            )
            self.file.flush()

    def finish(self):
        self.file.close()
