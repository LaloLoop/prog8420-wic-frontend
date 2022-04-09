from ._anvil_designer import CRUD_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .... import router as r

model = 'person' # change this for different CRUD_View forms

class CRUD_Person(CRUD_PersonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def button_nav_create_view_click(self, **event_args):
    r.get_crud_view_shower(model).show_view('create')
  def button_nav_read_view_click(self, **event_args):
    r.get_crud_view_shower(model).show_view('read')
  def button_nav_update_view_click(self, **event_args):
    r.get_crud_view_shower(model).show_view('update')
  def button_nav_delete_view_click(self, **event_args):
    r.get_crud_view_shower(model).show_view('delete')

  def button_nav_home_click(self, **event_args):
    email = dict(anvil.users.get_user())['email']
    # get the user's job title from person email
    user_job_title = 'admin' # assumed for now
    
    if user_job_title == 'admin':
      r.show_admin_home(self)
    elif user_job_title == 'staff':
      r.show_staff_home(self)
    elif user_job_title == 'doctor':
      r.show_doctor_home(self)







  





