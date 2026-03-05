
from cc3d import CompuCellSetup


from Base_SimulationSteppables import Base_SimulationSteppable
CompuCellSetup.register_steppable(steppable=Base_SimulationSteppable(frequency=1))

from Base_SimulationSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from Base_SimulationSteppables import CellGrowthSteppable
CompuCellSetup.register_steppable(steppable=CellGrowthSteppable(frequency=1))
        
from Base_SimulationSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))


CompuCellSetup.run()
