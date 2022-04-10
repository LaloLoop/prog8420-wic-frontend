from ._anvil_designer import Delete_PersonTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .... import router as r

model = 'person' # change this for different entities

class Delete_Person(Delete_PersonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.item['label_id_value'] = 'test'
    
    anvil.refresh_data_bindings()

    # Any code you write here will run when the form opens.

    
  def button_submit_click(self, **event_args):
    """This method is called when the button is clicked"""
    # use DELETE request to web api  
    
    # after successful submission,
    # redirect back to CRUD_Home
    r.get_crud_view_shower(model).show_view('crud', self)

