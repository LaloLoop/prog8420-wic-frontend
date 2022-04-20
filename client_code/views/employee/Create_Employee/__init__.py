from ._anvil_designer import Create_EmployeeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'employee'

class Create_Employee(Create_EmployeeTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator  

    self.validator.require(self.text_box_password_value,
                        ['change','lost_focus'],
                        lambda tb: tb.text != "",
                        self.label_password_value_invalid
                      )
    self.validator.enable_when_valid(self.button_submit)  

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ""
    url = f'{self.router.base_url}persons-unassigned'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)    
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    email = entity_id_to_fields[self.drop_down_person_id_value.selected_value]['email']

    url = f'{self.router.base_url}jobs'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    job_title = entity_id_to_fields[self.drop_down_job_id_value.selected_value]['title']

    #is_superuser = (job_title == 'admin') 
    
    data_dict = { 
      'person_id': int(self.drop_down_person_id_value.selected_value),
      'job_id': int(self.drop_down_job_id_value.selected_value),
      'email': email,
      'password': self.text_box_password_value.text,
      #'is_superuser': is_superuser,
      #'is_active': False,
      #'is_verified': False,
    }
    url = f'{self.router.base_url}auth/register'
    try:
      resp = self.http.request(url, method='POST', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    # use GET requests for list of persons and jobs_ids to populate all of the drop downs
    url = f'{self.router.base_url}persons-unassigned/'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)  
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    if not entity_id_to_fields:
      self.drop_down_person_id_value.include_placeholder = True
      self.drop_down_person_id_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_person_id_value.items = []
    else:
      self.drop_down_person_id_value.include_placeholder = False
      _ids = entity_id_to_fields.keys()
      self.drop_down_person_id_value.items = sorted( \
        [(entity_id_to_fields[_id]['email'], _id) for _id in _ids], key = lambda x: x[0])
      self.drop_down_person_id_value.selected_value = self.drop_down_person_id_value.items[0][1]
    
    self.validator.require(self.drop_down_person_id_value,
                      ['change'],
                      lambda dd: bool(dd.items),
                      self.label_person_id_value_invalid
                      )

    url = f'{self.router.base_url}jobs'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)      
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    if not entity_id_to_fields:
      self.drop_down_job_id_value.include_placeholder = True
      self.drop_down_job_id_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_job_id_value.items = []
    else:
      self.drop_down_job_id_value.include_placeholder = False
      _ids = entity_id_to_fields.keys()
      self.drop_down_job_id_value.items = sorted( \
        [(entity_id_to_fields[_id]['title'] + ", " + entity_id_to_fields[_id]['speciality'], 
        _id) for _id in _ids], key = lambda x: x[0])
      self.drop_down_job_id_value.selected_value = self.drop_down_job_id_value.items[0][1]
    
    self.validator.require(self.drop_down_job_id_value,
                      ['change'],
                      lambda dd: bool(dd.items),
                      self.label_job_id_value_invalid
                      )
    
    self.text_box_password_value.text = ""
    
    self.validator.show_all_errors()