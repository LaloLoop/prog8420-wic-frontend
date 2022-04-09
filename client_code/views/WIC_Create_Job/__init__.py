from ._anvil_designer import WIC_Create_JobTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.http

class WIC_Create_Job(WIC_Create_JobTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.item['title_dropdown'] = ['admin','staff','doctor'] # this will be grabbed from /job GET request
    self.item['speciality'] = 'cardiology'
    self.refresh_data_bindings()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    title = self.drop_down_1.selected_value
    speciality = self.text_box_1.text
    data_dict = {'title':title, 'speciality':speciality}
    
    resp = anvil.http.request('http://127.0.0.1:8000/job', method='POST', data=data_dict, json=True)
    
    print(resp)
    



