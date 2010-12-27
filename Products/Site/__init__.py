from site import Site, addForm, addAction

def initialize(registrar):
    registrar.registerClass(
        Site,
        constructors=(addForm, addAction),
        icon=None
        )
