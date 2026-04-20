from cc3d import CompuCellSetup


from DiffusionCoefficientCalculousSteppables import InitialConditionsSteppable

CompuCellSetup.register_steppable(steppable=InitialConditionsSteppable(frequency=1))

from DiffusionCoefficientCalculousSteppables import UnwrappedCOMTrackerSteppable

CompuCellSetup.register_steppable(steppable=UnwrappedCOMTrackerSteppable(frequency=1))

from DiffusionCoefficientCalculousSteppables import ShapeTrackerSteppable

CompuCellSetup.register_steppable(steppable=ShapeTrackerSteppable(frequency=100))


CompuCellSetup.run()
