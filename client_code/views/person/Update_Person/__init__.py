from ._anvil_designer import Update_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Update_Person(Update_PersonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

    # use GET request to programmatically make form from JSON, or setup manually?

  def button_submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    # use PUT request to web api

    # after successful submission,
    # redirect back to CRUD_Home
    self.router.nav_to_route_view(self, 'person', 'crud')

  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.router.nav_to_route_view(self, 'person', 'crud')


