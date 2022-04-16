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
    
    self.feedback_banner.visible = False
    
    user_data = None
    try:
      anvil.server.call("login", user, password)
      user_data = anvil.server.call("auth_request", f"{self.router.base_url}users/me", json=True)
      
      banner_color = '#a5d6a7'
      feedback = f"Welcome {user_data['email']}"
      
    except anvil.http.HttpError as e:
      banner_color = '#ff5252'
      if e.status == 500:
        feedback = f"({e.status}) We had a problem processing your request"
      else:
        feedback = f"({e.status}) Please check your credentials"
        
    self.feedback_banner.text = feedback
    self.feedback_banner.visible = True  
    self.feedback_banner.background = banner_color
    
    if user_data is not None:
      self.router.nav_to_route_view(self, 'home', 'admin')