from ._anvil_designer import Create_UnitTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from form_checker import validation

model_name = 'unit'

class Create_Unit(Create_UnitTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    
    self.validator = validation.Validator()
    self.validator.require(self.text_box_name_value,
                           ['change','lost_focus'],
                           lambda tb: tb.text != '',
                           self.label_name_value_invalid
                          )
    
    self.validator.enable_when_valid(self.button_submit)
    
    self.validator.show_all_errors()
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}/'
    data_dict = {'name':self.text_box_name_value.text}
    
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'
      
  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    self.text_box_name_value.text = ""
    
    self.validator.show_all_errors()