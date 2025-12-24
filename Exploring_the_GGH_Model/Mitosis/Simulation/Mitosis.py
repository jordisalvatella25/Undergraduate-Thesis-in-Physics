
from cc3d import CompuCellSetup
        

from MitosisSteppables import MitosisSteppable

CompuCellSetup.register_steppable(steppable=MitosisSteppable(frequency=1))


from MitosisSteppables import CellDivisionSteppable

CompuCellSetup.register_steppable(steppable=CellDivisionSteppable(frequency=1))


from MitosisSteppables import FilesOutputSteppable

CompuCellSetup.register_steppable(steppable=FilesOutputSteppable(frequency=10))


CompuCellSetup.run()
