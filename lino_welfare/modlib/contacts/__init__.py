from lino import ad
    
class App(ad.App):

    extends = 'lino.modlib.contacts'
    extends_models = ['contacts.Partner','contacts.Person','contacts.Company']