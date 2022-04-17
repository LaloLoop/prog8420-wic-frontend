from ._anvil_designer import Update_EmployeeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'employee'

class Update_Employee(Update_EmployeeTemplate):
  def __init__(self, router, httpc, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use PUT request to web api

    # after successful submission,
    # redirect back to CRUD_Home
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    
    url = f'{self.router.base_url}persons-unassigned'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    email = entity_id_to_fields[self.drop_down_person_id_value.selected_value]['email']

    url = f'{self.router.base_url}jobs'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    job_title = entity_id_to_fields[self.drop_down_job_id_value.selected_value]['title']

    data_dict = { 
      'person_id': int(self.drop_down_person_id_value.selected_value),
      'job_id': int(self.drop_down_job_id_value.selected_value),
      'email': email,
      'password': self.text_box_password_value.text,
      'is_superuser': self.check_box_is_superuser_value.checked,
      #'is_active': False,
      #'is_verified': False,
    }

    successful_request = False
    try:
      # use PATCH request to web api
      url = f'{self.router.base_url}auth/register'
      resp = self.http.request(url, method='PATCH', data=data_dict, json=True)
      successful_request = True
    except anvil.http.HttpError as e: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      
      resp = {'detail': f'Unable to update Employee'}

    if 'detail' not in resp.keys(): # detail means error
      # after successful submission, redirect back to CRUD_Home
      self.router.nav_to_route_view(self, model_name, 'crud')
      return
    elif not successful_request:
      validation_msg = f"{resp['detail']}"    
    else:
      validation_msg = ""
      for d in resp['detail']: 
        validation_msg += f"{d['loc'][1]}: {d['msg']}\n"
      
    self.label_validation_errors.text = validation_msg

  def form_show(self, **event_args):
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp) 
    
    # use GET requests for list of persons and jobs_ids
    # to populate all of the drop downs
    url = f'{self.router.base_url}persons-unassigned'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    self.label_validation_errors.text = ""    
    

    _ids = entity_id_to_fields.keys()
    self.drop_down_person_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['email'], _id) for _id in _ids] + \
      [(current_entity_id_to_fields[current_id]['email'], current_id)] \                                                                            
    , key = lambda x: x[0])
    
    self.drop_down_person_id_value.selected_value = current_entity_id_to_fields[current_id]['person-_id']
    
    url = f'{self.router.base_url}jobs'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_job_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['title'] + ", " + entity_id_to_fields[_id]['speciality'], _id) for _id in _ids] + \
      [(current_entity_id_to_fields[current_id]['title'] + ", " + current_entity_id_to_fields[current_id]['speciality'], current_id)] \                                                                                  
     , key = lambda x: x[0])
    
    self.drop_down_job_id_value.selected_value = current_entity_id_to_fields[current_id]['job_id']
    
    self.check_box_is_superuser_value.checked = current_entity_id_to_fields[current_id]['is_superuser']
    
    self.text_box_password_value.text = current_entity_id_to_fields[current_id]['password']


