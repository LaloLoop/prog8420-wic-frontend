from ._anvil_designer import Staff_HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .... import router as r

class Staff_Home(Staff_HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_crud_person_view_click(self, **event_args):
    r.get_crud_view_shower('person').show_view('crud', self)

  def button_logout_click(self, **event_args):
    pass


