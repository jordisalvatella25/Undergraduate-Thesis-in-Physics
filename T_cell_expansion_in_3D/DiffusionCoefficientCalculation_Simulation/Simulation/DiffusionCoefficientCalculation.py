from cc3d import CompuCellSetup


from DiffusionCoefficientCalculationSteppables import InitialConditionsSteppable

CompuCellSetup.register_steppable(steppable=InitialConditionsSteppable(frequency=1))

from DiffusionCoefficientCalculationSteppables import UnwrappedCOMTrackerSteppable

CompuCellSetup.register_steppable(steppable=UnwrappedCOMTrackerSteppable(frequency=1))

from DiffusionCoefficientCalculationSteppables import ShapeTrackerSteppable

CompuCellSetup.register_steppable(steppable=ShapeTrackerSteppable(frequency=100))


CompuCellSetup.run()
