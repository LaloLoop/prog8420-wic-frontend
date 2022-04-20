from ._anvil_designer import Delete_UnitTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'unit'

class Delete_Unit(Delete_UnitTemplate):
  def __init__(self, router, httpc,  **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ""
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'
    data_dict = {'name':self.label_name_value.text}
    try:
      resp = self.http.request(url, method='DELETE', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)
      
  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    _id = anvil.server.call('get_selected_entity_id')
    url = f"{self.router.base_url}{model_name}/{_id}"
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)
    
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    # populate form with current values of entity
    self.label_id_value.text = _id
    self.label_name_value.text = entity_id_to_fields[_id]['name']