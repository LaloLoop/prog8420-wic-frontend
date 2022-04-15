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

  def button_home_show(self, **event_args):
    url = f'{self.router.base_url}{model_name}s-with-id-display-name'
    resp = anvil.http.request(url, method='GET', json=True)
    
    # convert resp (list of dicts) into dict[id] = dict of fields
    entity_id_to_fields = {}
    
    for e in resp:
      e_id = e['id']
      del e['id']
      entity_id_to_fields[e_id] = {**e}

    display_fields = ['id','patient_display_name','staff_display_name',
                      'doctor_display_name', 'prescription_display_name',
                      'date_and_time', 'comments']
    table_columns = ['Id', 'Patient', 'Staff', 'Doctor', 'Prescription', 'Time', 'Comments']
    
    table_rows = []
    for _id in entity_id_fields.keys():
      table_rows.append({table_columns[i]:entity_id_fields[_id][f] for i,f in enumerate(display_fields)})
    self.repeating_panel_1.items = table_rows
    
    list_of_display_name_tuples = [(entity_id_to_fields[_id]['', _id]) for _id in sorted(entity_id_to_fields.keys())]
    self.drop_down_all_entities.items = list_of_display_name_tuples

  def drop_down_all_entities_change(self, **event_args):
    anvil.server.call('set_selected_entity_id', self.drop_down_all_entities.selected_value)
    self.button_read_view.enabled = True
    self.button_delete_view.enabled = True
    self.button_update_view.enabled = True
 


