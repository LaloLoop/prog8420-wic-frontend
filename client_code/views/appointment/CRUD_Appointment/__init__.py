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
  def __init__(self, router, httpc,  **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.data_grid_of_entities.role = 'wide'

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

  def drop_down_all_entities_change(self, **event_args):
    selected = self.drop_down_all_entities.selected_value
    anvil.server.call('set_selected_entity_id', selected)
    
    if selected != self.router.crud_dropdown_placeholder:
      self.button_read_view.enabled = True
      self.button_delete_view.enabled = True
      self.button_update_view.enabled = True
    else:
      self.button_read_view.enabled = False
      self.button_delete_view.enabled = False
      self.button_update_view.enabled = False
    
  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    url = f'{self.router.base_url}{model_name}s-with-id-display-name/'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)     
    # convert resp (list of dicts) into dict[id] = dict of fields (not including id)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    # display fields within each entity dict
    display_fields = ['patient_display_name', 'staff_display_name','doctor_display_name',
                      'prescription_display_name','date_and_time', 'comments']
    
    # populate data grid
    table_columns = ['Patient', 'Staff', 'Doctor', 'Prescription', 'Time', 'Comments']
    
    table_rows = [] # repeating_panel takes a list of dictionaries/rows
    for _id in [e['id'] for e in sorted(resp, key = lambda x: x['patient_display_name'])]:
      fields_dict = entity_id_to_fields[str(_id)]
      table_rows.append({col:fields_dict[f] for col,f in zip(table_columns,display_fields)})
  
    grid_col_widths = [230,200,200,100,100,100] 
    grid_cols=[{'id':col,
                'width':grid_col_widths[i], 
                'title':col,
                'data_key':col} for i,col in enumerate(table_columns)]
    
    # set the data grid width to the entire screen width
    self.data_grid_of_entities.rows_per_page = 3
    self.data_grid_of_entities.show_page_controls = True
    #self.data_grid_of_entities.width = sum(grid_col_widths)
    self.data_grid_of_entities.columns = grid_cols
    self.repeating_panel_of_entities.items = table_rows
  
    # populate dropdown
    list_of_display_name_tuples = sorted( \
      [(entity_id_to_fields[_id]['appointment_display_name'], _id)
       for _id in sorted(entity_id_to_fields.keys())], key = lambda x: x[0])
    
    self.drop_down_all_entities.include_placeholder = True
    self.drop_down_all_entities.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_all_entities.selected_value = self.router.crud_dropdown_placeholder
    self.drop_down_all_entities.items = list_of_display_name_tuples
    
    if self.drop_down_all_entities.selected_value == self.router.crud_dropdown_placeholder:
      self.button_read_view.enabled = False
      self.button_delete_view.enabled = False
      self.button_update_view.enabled = False