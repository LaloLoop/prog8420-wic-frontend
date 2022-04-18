from ._anvil_designer import Update_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'person'

class Update_Person(Update_PersonTemplate):
  def __init__(self, router, validator, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    self.validator = validator    
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use PUT request to web api
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'

    data_dict = {
      'first_name': self.text_box_first_name_value.text,
      'last_name': self.text_box_last_name_value.text,
      'birthdate': str(self.date_picker_birthdate_value.date),
      'street': self.text_box_street_value.text,
      'city': self.text_box_city_value.text,
      'province': self.drop_down_province_value.selected_value,
      'postalcode': self.text_box_postal_code_value.text,
      'email': self.text_box_email_value.text,
      'phone_number': self.text_box_phonenumber_value.text
    }
    
    try:
      resp = anvil.http.request(url, method='PUT', data=data_dict, json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""    
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}/{current_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.label_id_value.text = current_id
    
    self.text_box_first_name_value.text = current_entity_id_to_fields[current_id]['first_name']
    self.text_box_last_name_value.text = current_entity_id_to_fields[current_id]['last_name']
    
    self.date_picker_birthdate_value.date = current_entity_id_to_fields[current_id]['birthdate']
    
    self.text_box_street_value.text = current_entity_id_to_fields[current_id]['street']
    self.text_box_city_value.text = current_entity_id_to_fields[current_id]['city']
    
    url = f'{self.router.base_url}person-list-of-provinces'
    provinces = anvil.http.request(url, method='GET', json=True)
    
    self.drop_down_province_value.items = sorted([(p,p) for p in provinces], key = lambda x: x[0])
    
    self.drop_down_province_value.selected_value = current_entity_id_to_fields[current_id]['province'] 
    
    self.text_box_postal_code_value.text = current_entity_id_to_fields[current_id]['postalcode'] 
    self.text_box_email_value.text = current_entity_id_to_fields[current_id]['email'] 
    self.text_box_phonenumber_value.text = current_entity_id_to_fields[current_id]['phone_number'] 