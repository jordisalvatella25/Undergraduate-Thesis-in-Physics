
from cc3d import CompuCellSetup
        

from Dispersion_of_one_cell_type_into_the_mediumSteppables import Dispersion_of_one_cell_type_into_the_mediumSteppable
from Dispersion_of_one_cell_type_into_the_mediumSteppables import EnergyOutputSteppable

CompuCellSetup.register_steppable(steppable=Dispersion_of_one_cell_type_into_the_mediumSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=EnergyOutputSteppable(frequency=10))


CompuCellSetup.run()
