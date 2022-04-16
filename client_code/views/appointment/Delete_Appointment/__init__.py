from ._anvil_designer import Delete_AppointmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'appointment'

class Delete_Appointment(Delete_AppointmentTemplate):
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
    _id = anvil.server.call('get_selected_entity_id')
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    # populate form with current values of entity
    self.label_id_value.text = _id
    self.label_patient_id_value.text = entity_id_to_fields[_id]['patient_display_name']
    self.label_staff_id_value.text  = entity_id_to_fields[_id]['staff_display_name']
    self.label_doctor_id_value.text  = entity_id_to_fields[_id]['doctor_display_name']
    self.label_prescription_id_value.text  = entity_id_to_fields[_id]['prescription_display_name']
    self.label_date_and_time_value.text  = entity_id_to_fields[_id]['date_and_time']
    self.label_comments_value.text  = entity_id_to_fields[_id]['comments']