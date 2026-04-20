
from cc3d import CompuCellSetup


from Initial_SimulationSteppables import Initial_SimulationSteppable
CompuCellSetup.register_steppable(steppable=Initial_SimulationSteppable(frequency=1))

from Initial_SimulationSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from Initial_SimulationSteppables import CellGrowthSteppable
CompuCellSetup.register_steppable(steppable=CellGrowthSteppable(frequency=1))
        
from Initial_SimulationSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))

from Initial_SimulationSteppables import EnergiesTrackerSteppable
CompuCellSetup.register_steppable(steppable=EnergiesTrackerSteppable(frequency=10))

from Initial_SimulationSteppables import MovementTrackerSteppable
CompuCellSetup.register_steppable(steppable=MovementTrackerSteppable(frequency=20))


CompuCellSetup.run()
