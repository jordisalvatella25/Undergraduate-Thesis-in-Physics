
from cc3d import CompuCellSetup
        

from Cells_MixingSteppables import Cells_MixingSteppable
from Cells_MixingSteppables import EnergyOutputSteppable

CompuCellSetup.register_steppable(steppable=Cells_MixingSteppable(frequency=1))
CompuCellSetup.register_steppable(steppable=EnergyOutputSteppable(frequency=10))


CompuCellSetup.run()
