from ._anvil_designer import Update_PatientTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'patient'

class Update_Patient(Update_PatientTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator
    self.validator.require(self.text_box_ohip_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_ohip_number(tb.text),
                           self.label_ohip_value_invalid
                           )
    self.validator.enable_when_valid(self.button_submit) 

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ''
    # use PUT request to web api
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'

    data_dict = { \
      'person_id': self.drop_down_person_id_value.selected_value,
      'ohip': self.text_box_ohip_value.text
    }
    
    try:
      resp = self.http.request(url, method='PUT', data=data_dict, json=True)
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
    
    # use GET requests for list of unassigned persons
    # to populate all of the drop downs
    url = f'{self.router.base_url}persons-unassigned'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_person_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['email'], _id) for _id in _ids] + \
      [(current_entity_id_to_fields[current_id]['person_display_name'], \
        current_entity_id_to_fields[current_id]['person_id'])] \
      , key = lambda x: x[0])
  
    self.drop_down_person_id_value.selected_value = current_entity_id_to_fields[current_id]['person_id']
    
    self.text_box_ohip_value.text =  current_entity_id_to_fields[current_id]['ohip']
    
    self.validator.show_all_errors()