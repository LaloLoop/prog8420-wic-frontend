from ._anvil_designer import Read_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .... import router as r

model = 'person' # change this for different entities

class Read_Person(Read_PersonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
    # use GET request to programmatically make form from JSON, or setup manually?

  def button_nav_crud_view_click(self, **event_args):
    """This method is called when the button is clicked"""
    r.get_crud_view_shower(model).show_view('crud', self)
