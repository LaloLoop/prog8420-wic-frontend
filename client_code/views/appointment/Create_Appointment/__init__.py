from ._anvil_designer import Create_AppointmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'appointment'

class Create_Appointment(Create_AppointmentTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def drop_down_doctor_id_value_change(self, **event_args):
    doctor_id = self.drop_down_doctor_id_value.selected_value

    # use GET request for new appointments by docter id
    url = f'{self.router.base_url}{model_name}-available-date-and-times/{doctor_id}'
    resp = anvil.http.request(url, method='GET', json=True)
    self.drop_down_date_and_time_value.items = [(dt,dt) for dt in resp]
    self.refresh_data_bindings()
    
  def button_submit_click(self, **event_args):
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}'

    data_dict = { \
      'patient_id': self.drop_down_patient_id_value.selected_value,
      'staff_id': self.drop_down_staff_id_value.selected_value,
      'doctor_id': self.drop_down_doctor_id_value.selected_value,
      'prescription_id': self.drop_down_prescription_id_value.selected_value,
      'date_and_time': self.drop_down_date_and_time_value.selected_value,
      'comments': self.text_area_comments_value.text
    }
    
    successful_request = False
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      successful_request = True
    except: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      resp = {'detail': 'Appointment with this patient, or doctor and time, already exists.'}

    if 'detail' not in resp.keys(): # detail means error
      # after successful submission, redirect back to CRUD_Home
      self.router.nav_to_route_view(self, model_name, 'crud')
      return
    elif not successful_request:
      validation_msg = f"{resp['detail']}"    
    else:
      validation_msg = ""
      for d in resp['detail']: 
        validation_msg += f"{d['loc'][1]}: {d['msg']}\n"
      
    self.label_validation_errors.text = validation_msg

  def form_show(self, **event_args):
    # use GET requests for list of patients, staff, doctor, prescriptions
    # to populate all of the drop downs
    url = f'{self.router.base_url}patients-unbooked-with-id-display-name'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.drop_down_patient_id_value.include_placeholder = True
    self.drop_down_patient_id_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_patient_id_value.selected_value = self.router.crud_dropdown_placeholder
    
    _ids = sorted(entity_id_to_fields.keys())
    self.drop_down_patient_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], keys = lambda x: x[0])
    
    url = f'{self.router.base_url}employees-staff-with-id-display-name'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.drop_down_staff_id_value.include_placeholder = True
    self.drop_down_staff_id_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_staff_id_value.selected_value = self.router.crud_dropdown_placeholder
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_staff_id_value.items = sorted( \
      [(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], key = lambda x: x[0])

    url = f'{self.router.base_url}employees-doctor-with-id-display-name'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    self.drop_down_doctor_id_value.include_placeholder = True
    self.drop_down_doctor_id_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_doctor_id_value.selected_value = self.router.crud_dropdown_placeholder   
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_doctor_id_value.items = sorted(\
      [(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], key = lambda x: x[0])
    
    initial_doctor_id = self.drop_down_doctor_id_value.items[0][1]

    url = f'{self.router.base_url}prescriptions-with-id-display-name'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    self.drop_down_prescription_id_value.include_placeholder = True
    self.drop_down_prescription_id_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_prescription_id_value.selected_value = self.router.crud_dropdown_placeholder
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_prescription_id_value.items = sorted(\
      [(entity_id_to_fields[_id]['prescription_display_name'], _id) for _id in _ids], key = lambda x: x[0])
 
    url = f'{self.router.base_url}appointment-available-date-and-times/{initial_doctor_id}'
    date_and_times = anvil.http.request(url, method='GET', json=True)
    
    self.drop_down_date_and_time_value.include_placeholder = True
    self.drop_down_date_and_time_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_date_and_time_value.selected_value = self.router.crud_dropdown_placeholder    
    
    self.drop_down_date_and_time_value.items = sorted([(dt,dt) for dt in date_and_times], key = lambda x: x[0])
    
    self.text_area_comments_value.text = ""