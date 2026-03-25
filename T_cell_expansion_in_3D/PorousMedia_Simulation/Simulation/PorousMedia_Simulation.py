
from cc3d import CompuCellSetup


from PorousMedia_SimulationSteppables import PorousMedia_SimulationSteppable
CompuCellSetup.register_steppable(steppable=PorousMedia_SimulationSteppable(frequency=1))

from PorousMedia_SimulationSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from PorousMedia_SimulationSteppables import CellGrowthSteppable
CompuCellSetup.register_steppable(steppable=CellGrowthSteppable(frequency=1))
        
from PorousMedia_SimulationSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))

from PorousMedia_SimulationSteppables import EnergiesTrackerSteppable
CompuCellSetup.register_steppable(steppable=EnergiesTrackerSteppable(frequency=10))

from PorousMedia_SimulationSteppables import COM_and_VS_TrackerSteppable
CompuCellSetup.register_steppable(steppable=COM_and_VS_TrackerSteppable(frequency=10))


CompuCellSetup.run()
