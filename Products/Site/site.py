from AccessControl import ClassSecurityInfo

from Globals import InitializeClass
from Globals import DTMLFile

from OFS.Folder import Folder

from zope.interface import implements

from interface import ISite


class Site(Folder):
    """Simple site main class"""

    implements(ISite)

    meta_type = 'ZSite'

    manage_options=Folder.manage_options

    security = ClassSecurityInfo()

    def __init__(self, id, title):
        "initialise a new instance of Site"
        self.id = id
        self.title = title

    def isRoot(self, context, container):
        """Checking this folder is Root folder or not."""
        return context == container

    security.declarePublic('getMenu')
    def getMenuItems(self, context, first_item='Home'):
        "Returns the menu items"
        menu = self.menu_item(context, self, first_item, 'first')
        for folder in self.menu_items():
            try:
                folder = getattr(self, folder)
                menu = menu + self.menu_item(context, folder, folder.title)
            except:
                msg = "BadMenuItem: %s " % folder
                raise Exception(msg)
        print menu
        return menu

    def menu_item(self, context, folder, name, cls=''):
        obj = context
        if obj == folder:
            a_class = "active"
            item = '<li class="%s %s">%s</li>' % (cls, a_class, name)
        else:
            item = '<li class="%s"><a href="%s" title="%s">%s</a></li>' % (cls, folder.absolute_url(), name, name)
            while obj is not self:
                if obj == folder:
                    a_class = "menu_active"
                    item = '<li class="%s %s">%s</li>' % (cls, a_class, name)
                    break
                obj = obj.aq_parent
        return item

InitializeClass(Site)

# constructor pages. Only used when the product is added to a folder.

def createDefaultIndex(context):
    """Copying content form templates/index.pt to ZMI index_html Page Template"""

    # Creting default index_html
    f = open(ZOPE_HOME+'/Products/Site/templates/index.pt', 'r')
    default_content = f.read()
    f.close()
    index_html = context.manage_addProduct['PageTemplates'].manage_addPageTemplate(
        'index_html', text=default_content)

    # Creating frontpage content (frontpage.pt)
    f = open(ZOPE_HOME+'/Products/Site/templates/frontpage.pt', 'r')
    fontpage_content = f.read()
    f.close()
    context.manage_addProduct['PageTemplates'].manage_addPageTemplate(
        'frontpage.pt', text=fontpage_content)

def createDefaultMenuItems(context):
    """Creating elements needed for menu Items"""
    menu_items = """
return [
    'about',
    'contacts'
]
"""
    context.manage_addProduct['PythonScripts'].manage_addPythonScript('menu_items')
    context['menu_items'].ZPythonScript_edit('', menu_items)

    context.manage_addProduct['OFSP'].manage_addFolder('about', 'About')
    context.manage_addProduct['OFSP'].manage_addFolder('contacts', 'Contact us')


def addAction(self, id='', title='', REQUEST=None):
            "Add a Site to Zope."
            site = Site(id, title)
            self._setObject(id, site)

            # Add header and description properties.
            # For better SEO use in index_html:
            # <title tal:content="here/header">The title</title>
            site_root = getattr(self, id)
            site_root.manage_addProperty('header', '', 'string')
            site_root.manage_addProperty('description', '', 'text')

            # Creating default content
            createDefaultIndex(site_root)
            createDefaultMenuItems(site_root)

            if REQUEST is not None:
                return self.manage_main(self, REQUEST)

addForm = DTMLFile('templates/addForm',
                   globals()) # Get user id from this form

