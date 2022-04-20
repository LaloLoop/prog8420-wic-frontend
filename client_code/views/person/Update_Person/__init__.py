from ._anvil_designer import Update_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import date

model_name = 'person'

class Update_Person(Update_PersonTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator
    self.validator.require(self.text_box_first_name_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_first_or_last_name(tb.text),
                           self.label_first_name_value_invalid
                          )
    self.validator.require(self.text_box_last_name_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_first_or_last_name(tb.text),
                           self.label_last_name_value_invalid
                          )
    self.date_picker_birthdate_value.date = date.today()
    self.validator.require(self.date_picker_birthdate_value,
                           ['change'],
                           lambda dp: self.validator.check_valid_birthdate(dp.date),
                           self.label_birthdate_value_invalid
                          )    
    self.validator.require(self.text_box_street_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_street_or_city(tb.text),
                           self.label_street_value_invalid
                          )
    self.validator.require(self.text_box_city_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_street_or_city(tb.text),
                           self.label_city_value_invalid
                          )
    self.validator.require(self.text_box_postal_code_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_canadian_postalcode(tb.text, strictCapitalization=False, fixSpace=False),
                           self.label_postalcode_value_invalid
                          )
    self.validator.require(self.text_box_email_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_email(tb.text),
                           self.label_email_value_invalid
                          )
    self.validator.require(self.text_box_phonenumber_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_phonenumber(tb.text),
                           self.label_phonenumber_value_invalid
                          )  
    self.validator.enable_when_valid(self.button_submit)     

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ''
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
      resp = self.http.request(url, method='PUT', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""    
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}/{current_id}"
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.label_id_value.text = current_id
    
    self.text_box_first_name_value.text = current_entity_id_to_fields[current_id]['first_name']
    self.text_box_last_name_value.text = current_entity_id_to_fields[current_id]['last_name']
    
    self.date_picker_birthdate_value.date = current_entity_id_to_fields[current_id]['birthdate']
    
    self.text_box_street_value.text = current_entity_id_to_fields[current_id]['street']
    self.text_box_city_value.text = current_entity_id_to_fields[current_id]['city']
    
    url = f'{self.router.base_url}person-list-of-provinces'
    try:
      provinces = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)
    
    self.drop_down_province_value.items = sorted([(p,p) for p in provinces], key = lambda x: x[0])
    
    self.drop_down_province_value.selected_value = current_entity_id_to_fields[current_id]['province'] 
    
    self.text_box_postal_code_value.text = current_entity_id_to_fields[current_id]['postalcode'] 
    self.text_box_email_value.text = current_entity_id_to_fields[current_id]['email'] 
    self.text_box_phonenumber_value.text = current_entity_id_to_fields[current_id]['phone_number'] 
    
    self.validator.show_all_errors()