
from cc3d import CompuCellSetup


from TCellExpansionInPorousMedium3DSteppables import InitialConditionsSteppable
CompuCellSetup.register_steppable(steppable=InitialConditionsSteppable(frequency=1))

from TCellExpansionInPorousMedium3DSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from TCellExpansionInPorousMedium3DSteppables import TCellGrowthSteppable
CompuCellSetup.register_steppable(steppable=TCellGrowthSteppable(frequency=1))
        
from TCellExpansionInPorousMedium3DSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))

from TCellExpansionInPorousMedium3DSteppables import EnergiesTrackerSteppable
CompuCellSetup.register_steppable(steppable=EnergiesTrackerSteppable(frequency=100))

from TCellExpansionInPorousMedium3DSteppables import WallContactTrackerSteppable
CompuCellSetup.register_steppable(steppable=WallContactTrackerSteppable(frequency=100))

from TCellExpansionInPorousMedium3DSteppables import DivisionStructureTrackerSteppable
CompuCellSetup.register_steppable(steppable=DivisionStructureTrackerSteppable(frequency=100))

from TCellExpansionInPorousMedium3DSteppables import VSRatioAndDistanceTrackerSteppable
CompuCellSetup.register_steppable(steppable=VSRatioAndDistanceTrackerSteppable(frequency=100))


CompuCellSetup.run()
