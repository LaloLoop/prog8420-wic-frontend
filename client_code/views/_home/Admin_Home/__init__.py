from ._anvil_designer import Admin_HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Admin_Home(Admin_HomeTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router

    # Any code you write here will run when the form opens.

  def button_crud_person_click(self, **event_args):
    """This method is called when the button is clicked"""
    r.get_crud_view_shower('person').show_view('crud', self)
    
  def button_logout_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass








