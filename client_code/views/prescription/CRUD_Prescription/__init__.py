from ._anvil_designer import CRUD_PrescriptionTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'prescription'
#{'medication': 'Atorvastatin', 'quantity': 200, 'prescription_id': 1, 'id': 1, 'prescription_display_name': 'mg'}
class CRUD_Prescription(CRUD_PrescriptionTemplate):
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

  def button_home_show(self, **event_args):
    url = f'{self.router.base_url}{model_name}s_with_id_display_name'
    resp = anvil.http.request(url, method='GET', json=True)
    self.repeating_panel_1.items = resp
    anvil.server.call('set_prescriptions', resp)
    #list_of_display_name_tuples = [(e['name'], e['id']) for e in resp]
    #self.drop_down_all_entities.items = list_of_display_name_tuples

  def drop_down_all_entities_change(self, **event_args):
    anvil.server.call('set_selected_prescription_id', self.drop_down_all_entities.selected_value)
    print(anvil.server.call('get_selected_prescription'))
    self.button_read_view.enabled = True
    self.button_delete_view.enabled = True
    self.button_update_view.enabled = True
