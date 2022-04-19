from ._anvil_designer import Create_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from datetime import date

model_name = 'person'

class Create_Person(Create_PersonTemplate):
  def __init__(self, router, validator, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
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
    # Any code you write here will run when the form opens.
    
  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}/'

    data_dict = {
      'first_name': self.text_box_first_name_value.text,
      'last_name': self.text_box_last_name_value.text,
      'birthdate': self.date_picker_birthdate_value.date,
      'street': self.text_box_street_value.text,
      'city': self.text_box_city_value.text,
      'province': self.drop_down_province_value.selected_value,
      'postalcode': self.text_box_postal_code_value.text,
      'email': self.text_box_email_value.text,
      'phone_number': self.text_box_phonenumber_value.text
    }

    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    self.text_box_first_name_value.text = ""
    self.text_box_last_name_value.text = ""
    
    #  self.date_picker_birthdate_value.date = datetime.date.today()
    self.text_box_street_value.text = ""
    
    url = f'{self.router.base_url}person-list-of-provinces'
    provinces = anvil.http.request(url, method='GET', json=True)
    
    self.drop_down_province_value.selected_value = self.router.crud_dropdown_placeholder    
    
    self.drop_down_province_value.items = sorted([(p,p) for p in provinces], key = lambda x: x[0])
    
    self.drop_down_province_value.selected_value = self.drop_down_province_value.items[0][1]  
    
    self.text_box_postal_code_value.text = ""
    self.text_box_email_value.text = ""
    self.text_box_phonenumber_value.text = ""
    
    self.validator.show_all_errors()