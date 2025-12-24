
from cc3d import CompuCellSetup
        

from Inverted_Cell_SortingSteppables import Inverted_Cell_SortingSteppable
from Inverted_Cell_SortingSteppables import EnergyOutputSteppable

CompuCellSetup.register_steppable(steppable=Inverted_Cell_SortingSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=EnergyOutputSteppable(frequency=10))


CompuCellSetup.run()
