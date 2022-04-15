from ._anvil_designer import CRUD_PrescriptionTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'prescription'

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

  def drop_down_all_entities_change(self, **event_args):
    anvil.server.call('set_selected_entity_id', self.drop_down_all_entities.selected_value)
    if self.drop_down_all_entities.selected_value != self.router.crud_dropdown_placeholder:
      self.button_read_view.enabled = True
      self.button_delete_view.enabled = True
      self.button_update_view.enabled = True
  
  def form_show(self, **event_args):
    url = f'{self.router.base_url}{model_name}s-with-id-display-name'
    resp = anvil.http.request(url, method='GET', json=True)
    
    # convert resp (list of dicts) into dict[id] = dict of fields (not including id)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    # display fields within each entity dict
    display_fields = ['medication', 'quantity', 'unit_display_name']
    
    # populate data grid
    table_columns = ['Medication', 'Quantity', 'Unit']
    
    table_rows = [] # repeating_panel takes a list of dictionaries/rows
    for _id in entity_id_to_fields.keys():
      fields_dict = entity_id_to_fields[_id]
      table_rows.append({col:fields_dict[f] for col,f in zip(table_columns,display_fields)})
  
    #grid_col_widths = [200]
    grid_cols=[{'id':col,
                #'width':grid_col_widths[i], 
                'title':col,
                'data_key':col} for i,col in enumerate(table_columns)]
    
    # set the data grid width to the entire screen width
    self.data_grid_of_entities.rows_per_page = 10
    self.data_grid_of_entities.show_page_controls = True
    #self.data_grid_of_entities.width = sum(grid_col_widths)
    self.data_grid_of_entities.columns = grid_cols
    self.repeating_panel_of_entities.items = table_rows
    
    # populate dropdown
    list_of_display_name_tuples = \
      [(entity_id_to_fields[_id]['name'], _id)
       for _id in sorted(entity_id_to_fields.keys())]
    
    self.drop_down_all_entities.include_placeholder = True
    self.drop_down_all_entities.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_all_entities.selected_value = self.router.crud_dropdown_placeholder
    self.drop_down_all_entities.items = list_of_display_name_tuples
    
    if self.drop_down_all_entities.selected_value == self.router.crud_dropdown_placeholder:
      self.button_read_view.enabled = False
      self.button_delete_view.enabled = False
      self.button_update_view.enabled = False





