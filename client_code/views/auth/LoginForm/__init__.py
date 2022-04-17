from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LoginForm(LoginFormTemplate):
  def __init__(self, router, httpc,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.http = httpc
    self.router = router

  def reset_feedback(self):
    self.feedback_banner.visible = False
    self.feedback_banner.color = '#ffffff'
    self.feedback_banner.text = ''
    
  def reset_login_input(self):
    self.user_box.text = "gbuchanan@example.net"
    self.password_box.text = "admin"
    
  def signin_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = self.user_box.text
    password = self.password_box.text
    
    self.reset_feedback()
    
    user_role = None
    try:
      user_role = self.http.login(username, password)
      banner_color = '#a5d6a7'
      feedback = "Welcome!"
      
    except anvil.http.HttpError as e:
      banner_color = '#ff5252'
      feedback = f"({e.status}) Failed to login: {e.content}"
        
    self.feedback_banner.text = feedback
    self.feedback_banner.visible = True  
    self.feedback_banner.background = banner_color
    
    if user_role is not None:
      self.router.nav_to_route_view(self, 'home', user_role['title'])

  def card_1_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.reset_feedback()
    self.reset_login_input()

