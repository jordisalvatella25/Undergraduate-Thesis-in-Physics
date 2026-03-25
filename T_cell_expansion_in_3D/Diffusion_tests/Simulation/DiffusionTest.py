from cc3d import CompuCellSetup


from DiffusionTestSteppables import DiffusionTestSteppable

CompuCellSetup.register_steppable(steppable=DiffusionTestSteppable(frequency=1))


from DiffusionTestSteppables import DiffusionTrackerSteppable

CompuCellSetup.register_steppable(steppable=DiffusionTrackerSteppable(frequency=10))


from DiffusionTestSteppables import COM_TrackerSteppable

CompuCellSetup.register_steppable(steppable=COM_TrackerSteppable(frequency=10))


CompuCellSetup.run()
