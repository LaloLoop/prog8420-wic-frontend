from ._anvil_designer import Update_UnitTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'unit'

class Update_Unit(Update_UnitTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use PUT request to web api
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'
    data_dict = {'name':self.text_box_name_value.text}
    
    successful_request = False
    try:
      resp = anvil.http.request(url, method='PUT', data=data_dict, json=True)
      successful_request = True
    except: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      resp = {'detail':'Name: Unit with this name already exists.'}
    
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
    _id = anvil.server.call('get_selected_entity_id')
    url = f"{self.router.base_url}{model_name}/{_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
  
    # populate form with current values of entity
    self.label_validation_errors.text = ""
    self.label_id_value.text = _id
    self.text_box_name_value.text = entity_id_to_fields[_id]['name']



