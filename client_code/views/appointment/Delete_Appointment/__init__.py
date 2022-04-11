from ._anvil_designer import Delete_AppointmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'person'

class Delete_Appointment(Delete_AppointmentTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.item['label_id_value'] = 'test'

    self.refresh_data_bindings()

    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use DELETE request to web api

    # after successful submission,
    # redirect back to CRUD_Home
    self.router.nav_to_route_view(self, model_name, 'crud')
