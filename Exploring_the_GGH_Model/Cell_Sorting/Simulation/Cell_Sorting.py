
from cc3d import CompuCellSetup
        

from Cell_SortingSteppables import Cell_SortingSteppable
from Cell_SortingSteppables import EnergyOutputSteppable

CompuCellSetup.register_steppable(steppable=Cell_SortingSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=EnergyOutputSteppable(frequency=10))


CompuCellSetup.run()
