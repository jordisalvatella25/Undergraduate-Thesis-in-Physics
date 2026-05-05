
from cc3d import CompuCellSetup


from PressureTestInPorousMediumSteppables import InitialConditionsSteppable
CompuCellSetup.register_steppable(steppable=InitialConditionsSteppable(frequency=1))

from PressureTestInPorousMediumSteppables import TCellActivationSteppable
CompuCellSetup.register_steppable(steppable=TCellActivationSteppable(frequency=1))

from PressureTestInPorousMediumSteppables import TCellGrowthSteppable
CompuCellSetup.register_steppable(steppable=TCellGrowthSteppable(frequency=1))
        
from PressureTestInPorousMediumSteppables import TCellMitosisSteppable
CompuCellSetup.register_steppable(steppable=TCellMitosisSteppable(frequency=1))

from PressureTestInPorousMediumSteppables import PressurePercentilesTrackerSteppable
CompuCellSetup.register_steppable(steppable=PressurePercentilesTrackerSteppable(frequency=100))

from PressureTestInPorousMediumSteppables import EnergiesTrackerSteppable
CompuCellSetup.register_steppable(steppable=EnergiesTrackerSteppable(frequency=100))

from PressureTestInPorousMediumSteppables import WallContactTrackerSteppable
CompuCellSetup.register_steppable(steppable=WallContactTrackerSteppable(frequency=100))

from PressureTestInPorousMediumSteppables import DivisionStructureTrackerSteppable
CompuCellSetup.register_steppable(steppable=DivisionStructureTrackerSteppable(frequency=100))

from PressureTestInPorousMediumSteppables import VSRatioAndDistanceTrackerSteppable
CompuCellSetup.register_steppable(steppable=VSRatioAndDistanceTrackerSteppable(frequency=100))


CompuCellSetup.run()
