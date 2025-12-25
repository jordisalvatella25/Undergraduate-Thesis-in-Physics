
from cc3d import CompuCellSetup
        

from Mitosis_with_pressure_constraintSteppables import Mitosis_with_pressure_constraintSteppable

CompuCellSetup.register_steppable(steppable=Mitosis_with_pressure_constraintSteppable(frequency=1))


from Mitosis_with_pressure_constraintSteppables import CellDivisionSteppable

CompuCellSetup.register_steppable(steppable=CellDivisionSteppable(frequency=1))


from Mitosis_with_pressure_constraintSteppables import FilesOutputSteppable

CompuCellSetup.register_steppable(steppable=FilesOutputSteppable(frequency=10))


CompuCellSetup.run()
