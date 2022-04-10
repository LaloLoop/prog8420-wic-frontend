from ._anvil_designer import Staff_HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Staff_Home(Staff_HomeTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_crud_person_view_click(self, **event_args):
    self.router.nav_to_route_view(self, 'person', 'crud')

  def button_logout_click(self, **event_args):
    pass


