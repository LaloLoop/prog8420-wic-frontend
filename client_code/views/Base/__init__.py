from ._anvil_designer import BaseTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import router as r

class Base(BaseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run when the form opens.

  def label_wic_show(self, **event_args):
    """This method is called when the Label is shown on the screen"""
    # show initial login
    # use get request to get list of all possible job titles
    allowed_job_titles = ['admin','staff','doctor']
    
    # use get request to check user's job title
    email_to_job_title = {'q@q.qq':'admin', 'a@a.aa':'not_admin'}

    job_title = '' # dummy to enter while
    while job_title not in allowed_job_titles:
      anvil.users.logout()
      self.label_logged_in_welcome_message.text = ""
      
      anvil.users.login_with_form()
      
      user_table_row = anvil.users.get_user() # returns <LiveObject: anvil.tables.Row>
      
      email = dict(user_table_row)['email']
      
      self.label_logged_in_welcome_message.text = f"{email} is logged in"
      
      job_title = email_to_job_title[email]
    
      if job_title in allowed_job_titles:
        break;
    
    if job_title == 'admin':
      r.show_admin_home_after_login()
    elif job_title == 'staff':
      r.show_staff_home_after_login()
    elif job_title == 'doctor':
      r.show_doctor_home_after_login()

