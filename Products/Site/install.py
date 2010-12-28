from Globals import DTMLFile

from site import Site

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
    f = open(ZOPE_HOME+'/Products/Site/templates/about.pt', 'r')
    about_content = f.read()
    f.close()
    context['about'].manage_addProduct['PageTemplates'].manage_addPageTemplate(
        'body.pt', text=about_content)

    context.manage_addProduct['OFSP'].manage_addFolder('contacts', 'Contact us')
    f = open(ZOPE_HOME+'/Products/Site/templates/contacts.pt', 'r')
    about_content = f.read()
    f.close()
    contacts = context['contacts']
    contacts.manage_addProduct['PageTemplates'].manage_addPageTemplate(
        'body.pt', text=about_content)

    # Creating send Python script for mail sending.
    send_script = """
To = "info@example.com"
request = context.REQUEST
return container.sendEmail (request, To)
"""
    contacts.manage_addProduct['PythonScripts'].manage_addPythonScript('send')
    contacts['send'].ZPythonScript_edit('', send_script)

def createMailHost(context):
    """Create MailHost for email sending from Zope"""
    context.manage_addProduct['MailHost'].manage_addMailHost('MailHost', smtp_host='localhost')

def createJS(context):
    context.manage_addProduct['OFSP'].manage_addFolder('js', 'JavaScript')
    file = open(ZOPE_HOME+'/Products/Site/js/default.js', 'r')
    context['js'].manage_addProduct['OFSP'].manage_addFile('default.js', file=file.read())
    file.close()

    file = open(ZOPE_HOME+'/Products/Site/js/jquery-1.4.4.min.js', 'r')
    context['js'].manage_addProduct['OFSP'].manage_addFile('jquery-1.4.4.min.js', file=file.read())
    file.close()

# constructor pages. Only used when the product is added to a folder.

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
            createMailHost(site_root)
            createJS(site_root)

            if REQUEST is not None:
                return self.manage_main(self, REQUEST)

addForm = DTMLFile('templates/addForm',
                   globals()) # Get user id from this form
