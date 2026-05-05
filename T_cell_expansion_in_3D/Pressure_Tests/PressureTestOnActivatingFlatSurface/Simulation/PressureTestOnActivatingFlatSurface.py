
from cc3d import CompuCellSetup


from PressureTestOnActivatingFlatSurfaceSteppables import InitialConditionsSteppable
CompuCellSetup.register_steppable(steppable=InitialConditionsSteppable(frequency=1))

from PressureTestOnActivatingFlatSurfaceSteppables import HeightMonitoringSteppable
CompuCellSetup.register_steppable(steppable=HeightMonitoringSteppable(frequency=1))

from PressureTestOnActivatingFlatSurfaceSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from PressureTestOnActivatingFlatSurfaceSteppables import TCellGrowthSteppable
CompuCellSetup.register_steppable(steppable=TCellGrowthSteppable(frequency=1))
        
from PressureTestOnActivatingFlatSurfaceSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))

from PressureTestOnActivatingFlatSurfaceSteppables import PressurePercentilesTrackerSteppable
CompuCellSetup.register_steppable(steppable=PressurePercentilesTrackerSteppable(frequency=100))

from PressureTestOnActivatingFlatSurfaceSteppables import EnergiesTrackerSteppable
CompuCellSetup.register_steppable(steppable=EnergiesTrackerSteppable(frequency=100))

from PressureTestOnActivatingFlatSurfaceSteppables import WallContactTrackerSteppable
CompuCellSetup.register_steppable(steppable=WallContactTrackerSteppable(frequency=100))

from PressureTestOnActivatingFlatSurfaceSteppables import DivisionStructureTrackerSteppable
CompuCellSetup.register_steppable(steppable=DivisionStructureTrackerSteppable(frequency=100))

from PressureTestOnActivatingFlatSurfaceSteppables import VSRatioAndDistanceTrackerSteppable
CompuCellSetup.register_steppable(steppable=VSRatioAndDistanceTrackerSteppable(frequency=100))


CompuCellSetup.run()
