from ._anvil_designer import Delete_PrescriptionTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'prescription'

class Delete_Prescription(Delete_PrescriptionTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use DELETE request to web api
    url = f"{self.router.base_url}{model_name}/{self.label_id_value.text}"
    
    try:
      resp = anvil.http.request(url, method='DELETE', json=True)
    except: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      self.label_validation_errors.text = "unsuccessful delete"
      return
    self.router.nav_to_route_view(self, model_name, 'crud')

  def form_show(self, **event_args):
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    self.label_validation_errors.text = ""    
    self.label_id_value.text = current_id
    self.label_medication_value.text = current_entity_id_to_fields[current_id]['medication']
    self.label_quantity_value.text = current_entity_id_to_fields[current_id]['quantity']
    self.label_unit_id_value.text = current_entity_id_to_fields[current_id]['unit_display_name']

