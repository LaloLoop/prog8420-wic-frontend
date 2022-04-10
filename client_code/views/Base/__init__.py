from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Base(BaseTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    

    # Any code you write here will run when the form opens.

  def label_wic_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    self.router.nav_to_route_view(self, 'home','admin')


