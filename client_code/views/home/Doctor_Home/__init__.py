from ._anvil_designer import Doctor_HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Doctor_Home(Doctor_HomeTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router

    # Any code you write here will run when the form opens.

  def button_nav_crud_prescription_view_click(self, **event_args):
    self.router.nav_to_route_view(self, 'prescription', 'crud')

  def button_logout_click(self, **event_args):
    pass






