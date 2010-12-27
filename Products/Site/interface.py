from zope.interface import Interface

class ISite(Interface):
    """Simple site"""

    def getMenuItems():
        """Get site's Hello"""

