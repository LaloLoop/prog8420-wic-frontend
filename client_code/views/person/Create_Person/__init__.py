from ._anvil_designer import Create_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'person'

class Create_Person(Create_PersonTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.
    
  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}'

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
    
    successful_request = False
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      successful_request = True
    except: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      resp = {'detail': 'Person with this Email already exists?'}

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
    self.label_validation_errors.text = ""
    self.text_box_first_name_value.text = ""
    self.text_box_last_name_value.text = ""
    
    import datetime
    self.date_picker_birthdate_value.date = datetime.date.today()
    
    self.text_box_street_value.text = ""
    
    url = f'{self.router.base_url}person-list-of-provinces'
    provinces = anvil.http.request(url, method='GET', json=True)
    
    self.drop_down_province_value.include_placeholder = True
    self.drop_down_province_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_province_value.selected_value = self.router.crud_dropdown_placeholder    
    
    self.drop_down_province_value.items = sorted([(p,p) for p in provinces], key = lambda x: x[0])
    
    self.text_box_postal_code_value.text = ""
    self.text_box_email_value.text = ""
    self.text_box_phonenumber_value.text = ""