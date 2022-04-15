from ._anvil_designer import Create_UnitTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'unit'

class Create_Unit(Create_UnitTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use POST request to web api
    data_dict = {'name':self.text_box_name_value.text}
    url = f'{self.router.base_url}{model_name}'
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
    except: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      resp = {'detail':'Name: Unit with this name already exists.'}
      
    if 'detail' not in resp.keys(): # detail means error
      # after successful submission, redirect back to CRUD_Home
      self.router.nav_to_route_view(self, model_name, 'crud')
    else:
      validation_msg = f"{resp['detail']}"
      self.label_validation_errors.text = validation_msg