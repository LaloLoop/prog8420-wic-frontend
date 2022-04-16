from ._anvil_designer import Create_PatientTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'patient'

class Create_Patient(Create_PatientTemplate):
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
      'person_id': self.drop_down_person_id_value.selected_value,
      'ohip': self.text_box_ohip_value.text
    }
    
    successful_request = False
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      successful_request = True
    except: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      resp = {'detail': 'Unable to create Patient'}

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
    # use GET requests for list of unassigned persons
    # to populate all of the drop downs
    url = f'{self.router.base_url}persons-unassigned'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.drop_down_person_id_value.include_placeholder = True
    self.drop_down_person_id_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_person_id_value.selected_value = self.router.crud_dropdown_placeholder
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_person_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['email'], _id) for _id in _ids], key = lambda x: x[0])
    
    self.text_box_ohip_value.text = ""