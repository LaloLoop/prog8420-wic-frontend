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
    # use POST request to web api
    name = self.text_box_name_value.text
    unit_id = self.label_id_value.text
    data_dict = {'name':name}
    
    url = f'{self.router.base_url}{model_name}/{unit_id}'
    
    self.label_validation_errors.text = str(data_dict)
    self.label_validation_errors.text = url
    resp = anvil.http.request(url, method='PUT', data=data_dict, json=True)
    # after successful submission,
    # redirect back to CRUD_Home
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_back_show(self, **event_args):
    selected_unit = anvil.server.call('get_selected_unit')
    self.label_id_value.text = selected_unit['id']
    self.text_box_name_value.text = selected_unit['name']

