from ._anvil_designer import WIC_Create_JobTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.http

class WIC_Create_Job(WIC_Create_JobTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.item['title_dropdown'] = ['admin','staff','doctor']
    self.item['speciality'] = 'cardiology'
    self.refresh_data_bindings()
    
    # Any code you write here will run when the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""

    anvil.http.request(url, method='GET',)
    
  def drop_down_1_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    
    






