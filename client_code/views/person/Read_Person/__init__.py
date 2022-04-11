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
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    
    # GET request 
    #anvil.http.request()
    #resp = anvil.http.request('http://127.0.0.1:8000/person', method='GET', json=True)
    #resp['title']
    #resp['id']
    
    self.item['label_id_value_text'] = 'From GET Request' # resp['id']
    self.refresh_data_bindings()

    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')
