from ._anvil_designer import Update_EmployeeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'employee'

class Update_Employee(Update_EmployeeTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    self.label_validation_errors = ""
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)  
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp) 
  
    data_dict = { 
      'job_id': self.drop_down_job_id_value.selected_value,
      'is_superuser': self.check_box_is_superuser_value.checked,
    }    
    
    if self.text_box_password_value.text != "":
      data_dict['password'] = self.text_box_password_value.text,

    url = f'{self.router.base_url}users/{current_id}'
    try:
      resp = self.http.request(url, method='PATCH', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)  

  def form_show(self, **event_args):
    self.label_validation_errors.text = "" 
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)     
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp) 

    self.label_id_value.text = current_id
    self.label_person_id_value.text = current_entity_id_to_fields[current_id]['person_display_name']
    
    url = f'{self.router.base_url}jobs'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)  
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_job_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['title'] + ", " + entity_id_to_fields[_id]['speciality'], _id) for _id in _ids] 
      , key = lambda x: x[0])
    
    self.drop_down_job_id_value.selected_value = str(current_entity_id_to_fields[current_id]['job_id'])
    
    self.text_box_password_value.text = ""
    self.check_box_is_superuser_value.checked = current_entity_id_to_fields[current_id]['is_superuser']    