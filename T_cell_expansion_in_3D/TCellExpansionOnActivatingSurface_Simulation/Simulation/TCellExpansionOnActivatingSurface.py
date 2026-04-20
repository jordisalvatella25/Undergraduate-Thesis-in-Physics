
from cc3d import CompuCellSetup


from TCellExpansionOnActivatingSurfaceSteppables import InitialConditionsSteppable
CompuCellSetup.register_steppable(steppable=InitialConditionsSteppable(frequency=1))

from TCellExpansionOnActivatingSurfaceSteppables import HeightMonitoringSteppable
CompuCellSetup.register_steppable(steppable=HeightMonitoringSteppable(frequency=1))

from TCellExpansionOnActivatingSurfaceSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from TCellExpansionOnActivatingSurfaceSteppables import TCellGrowthSteppable
CompuCellSetup.register_steppable(steppable=TCellGrowthSteppable(frequency=1))
        
from TCellExpansionOnActivatingSurfaceSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))

from TCellExpansionOnActivatingSurfaceSteppables import EnergiesTrackerSteppable
CompuCellSetup.register_steppable(steppable=EnergiesTrackerSteppable(frequency=100))

from TCellExpansionOnActivatingSurfaceSteppables import WallContactTrackerSteppable
CompuCellSetup.register_steppable(steppable=WallContactTrackerSteppable(frequency=100))

from TCellExpansionOnActivatingSurfaceSteppables import DivisionStructureTrackerSteppable
CompuCellSetup.register_steppable(steppable=DivisionStructureTrackerSteppable(frequency=100))

from TCellExpansionOnActivatingSurfaceSteppables import VSRatioAndDistanceTrackerSteppable
CompuCellSetup.register_steppable(steppable=VSRatioAndDistanceTrackerSteppable(frequency=100))


CompuCellSetup.run()
