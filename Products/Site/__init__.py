from install import addForm, addAction
from site import Site

def initialize(registrar):
    registrar.registerClass(
        Site,
        constructors=(addForm, addAction),
        icon=None
        )
