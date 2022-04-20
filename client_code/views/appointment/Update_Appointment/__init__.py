from ._anvil_designer import Update_AppointmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'appointment'

class Update_Appointment(Update_AppointmentTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')
    
  def drop_down_doctor_id_value_change(self, **event_args):
    self.label_validation_errors.text = ""
    doctor_id = self.drop_down_doctor_id_value.selected_value

    # use GET request for new appointments by docter id
    url = f'{self.router.base_url}{model_name}-available-date-and-times/{doctor_id}'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    self.drop_down_date_and_time.items = [(dt,dt) for dt in resp]
    self.refresh_data_bindings()
    
  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ""
    # use PUT request to web api
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'

    data_dict = { \
      'patient_id': self.drop_down_patient_id_value.selected_value,
      'staff_id': self.drop_down_staff_id_value.selected_value,
      'doctor_id': self.drop_down_doctor_id_value.selected_value,
      'prescription_id': int(self.drop_down_prescription_id_value.selected_value),
      'date_and_time': self.drop_down_date_and_time_value.selected_value,
      'comments': self.text_area_comments_value.text
    }
    
    try:
      resp = self.http.request(url, method='PUT', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.label_id_value.text = current_id
    
    # use GET requests for list of patients, staff, doctor, prescriptions
    # to populate all of the drop downs
    url = f'{self.router.base_url}patients-unbooked-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)     
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    _ids = entity_id_to_fields.keys()
    self.drop_down_patient_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids] + \
      [(current_entity_id_to_fields[current_id]['patient_display_name'], \
        current_entity_id_to_fields[current_id]['patient_id'])] \ 
      ,key = lambda x: x[0] )
      
    self.drop_down_patient_id_value.selected_value = current_entity_id_to_fields[current_id]['patient_id']
    
    url = f'{self.router.base_url}employees-staff-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    _ids = entity_id_to_fields.keys()
    self.drop_down_staff_id_value.items = \
      sorted([(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], key = lambda x: x[0])

    self.drop_down_staff_id_value.selected_value = current_entity_id_to_fields[current_id]['staff_id']
    
    url = f'{self.router.base_url}employees-doctor-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    _ids = entity_id_to_fields.keys()
    self.drop_down_doctor_id_value.items = \
      sorted([(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], key = lambda x: x[0])

    self.drop_down_doctor_id_value.selected_value = current_entity_id_to_fields[current_id]['doctor_id']
    
    initial_doctor_id = list(_ids)[0]

    url = f'{self.router.base_url}prescriptions-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    _ids = entity_id_to_fields.keys()
    self.drop_down_prescription_id_value.items = \
      sorted([(entity_id_to_fields[_id]['prescription_display_name'], _id) for _id in _ids], key = lambda x: x[0])
 
    self.drop_down_prescription_id_value.selected_value = str(current_entity_id_to_fields[current_id]['prescription_id'])

    url = f'{self.router.base_url}appointment-available-date-and-times/{initial_doctor_id}'
    try:
      date_and_times = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    self.drop_down_date_and_time_value.items = sorted( \
      [(dt,dt) for dt in date_and_times] + \
      [(current_entity_id_to_fields[current_id]['date_and_time'], \
        current_entity_id_to_fields[current_id]['date_and_time'])] \
      ,key= lambda x: x[0] )
    self.drop_down_date_and_time_value.selected_value = current_entity_id_to_fields[current_id]['date_and_time']