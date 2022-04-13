from ._anvil_designer import Create_PrescriptionTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'prescription'

class Create_Prescription(Create_PrescriptionTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use POST request to web api
    medication = self.text_box_medication_value.text
    quantity = self.text_box_quantity_value.text
    unit_id = self.drop_down_unit_id_value.selected_value
    data_dict = {'medication':medication, 'quantity': quantity, 'unit_id': unit_id}   
    
    url = f'{self.router.base_url}{model_name}'

    resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
    print(resp)
    # after successful submission,
    # redirect back to CRUD_Home
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_back_show(self, **event_args):
    url = f'{self.router.base_url}units'
    resp = anvil.http.request(url, method='GET', json=True)

    list_of_display_name_tuples = [(e['name'], e['id']) for e in resp]
    self.drop_down_unit_id_value.items = list_of_display_name_tuples
    


