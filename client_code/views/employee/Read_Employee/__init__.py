from ._anvil_designer import Read_EmployeeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'employee'

class Read_Employee(Read_EmployeeTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def form_show(self, **event_args):
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp) 
  
    self.label_person_id_value.selected_value = current_entity_id_to_fields[current_id]['person_id']
    
    self.label_job_id_value.selected_value = current_entity_id_to_fields[current_id]['job_id']
    
    self.label_password.text =  len(current_entity_id_to_fields[current_id]['password'])
    
    self.label_is_active_value.checked = current_entity_id_to_fields[current_id]['is_active']
    self.label_is_verified_value.checked = current_entity_id_to_fields[current_id]['is_verified']
    self.label_is_superuser_value.checked = current_entity_id_to_fields[current_id]['is_superuser']