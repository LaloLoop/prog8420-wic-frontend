from ._anvil_designer import Update_AppointmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'appointment'

class Update_Appointment(Update_AppointmentTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def drop_down_doctor_id_value_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
    
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    # use PUT request to web api

    # after successful submission,
    # redirect back to CRUD_Home
    self.router.nav_to_route_view(self, model_name, 'crud')

  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    pass





