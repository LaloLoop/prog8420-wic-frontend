from ._anvil_designer import Delete_EmployeeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'employee'

class Delete_Employee(Delete_EmployeeTemplate):
  def __init__(self, router, httpc, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use DELETE request to web api
    url = f"{self.router.base_url}users/{self.label_id_value.text}"
    
    try:
      resp = self.http.request(url, method='DELETE', json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'


  def form_show(self, **event_args):
    current_id = anvil.server.call('get_selected_entity_id')
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp) 

    self.label_id_value.text = current_id
    self.label_person_id_value.text = current_entity_id_to_fields[current_id]['person_display_name']
    self.label_job_id_value.text = current_entity_id_to_fields[current_id]['job_display_name']
    self.label_password_value.text =  '*************'
    self.label_is_active_value.text = str(current_entity_id_to_fields[current_id]['is_active'])
    self.label_is_verified_value.text = str(current_entity_id_to_fields[current_id]['is_verified'])
    self.label_is_superuser_value.text = str(current_entity_id_to_fields[current_id]['is_superuser'])