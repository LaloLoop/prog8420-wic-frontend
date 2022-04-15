from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LoginForm(LoginFormTemplate):
  def __init__(self, router,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.router = router

    # Any code you write here will run when the form opens.

  def signin_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = self.user_box.text
    password = self.password_box.text
    
    

