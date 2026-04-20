
from cc3d import CompuCellSetup


from PorousMedia_SimulationSteppables import InitialConditionsSteppable
CompuCellSetup.register_steppable(steppable=InitialConditionsSteppable(frequency=1))

from PorousMedia_SimulationSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from PorousMedia_SimulationSteppables import CellGrowthSteppable
CompuCellSetup.register_steppable(steppable=CellGrowthSteppable(frequency=1))
        
from PorousMedia_SimulationSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))

from PorousMedia_SimulationSteppables import EnergiesTrackerSteppable
CompuCellSetup.register_steppable(steppable=EnergiesTrackerSteppable(frequency=100))

from PorousMedia_SimulationSteppables import VSRatioAndDistanceTrackerSteppable
CompuCellSetup.register_steppable(steppable=VSRatioAndDistanceTrackerSteppable(frequency=10))


CompuCellSetup.run()
