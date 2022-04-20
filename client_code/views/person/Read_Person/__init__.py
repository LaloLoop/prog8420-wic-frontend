from ._anvil_designer import Read_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.http
model_name = 'person'

class Read_Person(Read_PersonTemplate):
  def __init__(self, router, httpc, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')
  
  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    _id = anvil.server.call('get_selected_entity_id')
    try:
      url = f"{self.router.base_url}{model_name}/{_id}"
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)

    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.label_id_value.text = _id
    self.label_first_name_value.text = entity_id_to_fields[_id]['first_name']
    self.label_last_name_value.text = entity_id_to_fields[_id]['last_name']
    self.label_birthdate_value.text = entity_id_to_fields[_id]['birthdate']
    self.label_street_value.text = entity_id_to_fields[_id]['street']
    self.label_city_value.text = entity_id_to_fields[_id]['city']
    self.label_province_value.text = entity_id_to_fields[_id]['province']
    self.label_postalcode_value.text = entity_id_to_fields[_id]['postalcode']
    self.label_email_value.text = entity_id_to_fields[_id]['email']
    self.label_phonenumber_value.text = entity_id_to_fields[_id]['phone_number']