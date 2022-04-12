from ._anvil_designer import CRUD_AppointmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.http
model_name = 'appointment'

class CRUD_Appointment(CRUD_AppointmentTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_nav_create_view_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'create')
    
  def button_nav_read_view_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'read')
    
  def button_nav_update_view_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'update')
    
  def button_nav_delete_view_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'delete')

  def button_nav_home_click(self, **event_args):
    self.router.nav_to_route_view(self, 'home', 'admin')

  def label_selected_entity_show(self, **event_args):
    #GET
    url = f'{self.router.base_url}{model_name}s_with_id_display_name'
    
    resp = anvil.http.request(urls, method='GET', json=True)
    
    self.label_validation_errors.text = str(resp)
    
    #self.drop_down_all_entities.items =

