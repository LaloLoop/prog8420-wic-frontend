from ._anvil_designer import Update_UnitTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'unit'

class Update_Unit(Update_UnitTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator
    self.validator.require(self.text_box_name_value,
                           ['change','lost_focus'],
                           lambda tb: 1 <= len(tb.text) <= 10,
                           self.label_name_value_invalid
                          )
    self.validator.enable_when_valid(self.button_submit)

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ''
    # use PUT request to web api
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'
    data_dict = {'name':self.text_box_name_value.text}
    
    try:
      resp = self.http.request(url, method='PUT', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = self.http.get_error_message(e)

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    _id = anvil.server.call('get_selected_entity_id')
    url = f"{self.router.base_url}{model_name}/{_id}"
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = self.http.get_error_message(e)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
  
    # populate form with current values of entity
    self.label_id_value.text = _id
    self.text_box_name_value.text = entity_id_to_fields[_id]['name']
