from ._anvil_designer import Create_AppointmentTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'appointment'

class Create_Appointment(Create_AppointmentTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator
    
    self.validator.enable_when_valid(self.button_submit)  

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def drop_down_doctor_id_value_change(self, **event_args):
    self.label_validation_errors.text = ""
    doctor_id = self.drop_down_doctor_id_value.selected_value

    # use GET request for new appointments by docter id
    url = f'{self.router.base_url}{model_name}-available-date-and-times/{doctor_id}'
    try:
      date_and_times = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)    
    self.drop_down_date_and_time_value.items = [(dt,dt) for dt in date_and_times]
    self.refresh_data_bindings()
    
  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ""
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}/'

    data_dict = { \
      'patient_id': self.drop_down_patient_id_value.selected_value,
      'staff_id': self.drop_down_staff_id_value.selected_value,
      'doctor_id': self.drop_down_doctor_id_value.selected_value,
      'prescription_id': self.drop_down_prescription_id_value.selected_value,
      'date_and_time': self.drop_down_date_and_time_value.selected_value,
      'comments': self.text_area_comments_value.text
    }
    
    try:
      resp = self.http.request(url, method='POST', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    
    # use GET requests for list of patients, staff, doctor, prescriptions
    # to populate all of the drop downs
    url = f'{self.router.base_url}patients-unbooked-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)     
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    if not entity_id_to_fields:
      self.drop_down_patient_id_value.include_placeholder = True
      self.drop_down_patient_id_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_patient_id_value.items = []
    else:
      self.drop_down_patient_id_value.include_placeholder = False
      _ids = entity_id_to_fields.keys()
      self.drop_down_patient_id_value.items = sorted( \
        [(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], key = lambda x: x[0])
      self.drop_down_patient_id_value.selected_value = self.drop_down_patient_id_value.items[0][1]
    
    self.validator.require(self.drop_down_patient_id_value,
                          ['change'],
                          lambda dd: bool(dd.items),
                          self.label_patient_id_value_invalid
                          )    

    url = f'{self.router.base_url}employees-staff-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    if not entity_id_to_fields:
      self.drop_down_staff_id_value.include_placeholder = True
      self.drop_down_staff_id_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_staff_id_value.items = []
    else:
      self.drop_down_staff_id_value.include_placeholder = False
      _ids = entity_id_to_fields.keys()
      self.drop_down_staff_id_value.items = sorted( \
        [(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], key = lambda x: x[0])
      self.drop_down_staff_id_value.selected_value = self.drop_down_staff_id_value.items[0][1]
    
    self.validator.require(self.drop_down_staff_id_value,
                          ['change'],
                          lambda dd: bool(dd.items),
                          self.label_staff_id_value_invalid,
                          )

    url = f'{self.router.base_url}employees-doctor-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
 
    initial_doctor_id = "" # only populate date_and_time drop down if doctors available
    if not entity_id_to_fields:
      self.drop_down_doctor_id_value.include_placeholder = True
      self.drop_down_doctor_id_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_doctor_id_value.items = []
    else:
      self.drop_down_doctor_id_value.include_placeholder = False
      _ids = entity_id_to_fields.keys()
      self.drop_down_doctor_id_value.items = sorted( \
        [(entity_id_to_fields[_id]['person_display_name'], _id) for _id in _ids], key = lambda x: x[0])
      
      initial_doctor_id = self.drop_down_doctor_id_value.items[0][1]
      self.drop_down_doctor_id_value.selected_value = initial_doctor_id
    
    self.validator.require(self.drop_down_doctor_id_value,
                      ['change'],
                      lambda dd: bool(dd.items),
                      self.label_doctor_id_value_invalid
                          )

    url = f'{self.router.base_url}prescriptions-with-id-display-name'
    try:
      resp = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e) 
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    if not entity_id_to_fields:
      self.drop_down_prescription_id_value.include_placeholder = True
      self.drop_down_prescription_id_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_prescription_id_value.items = []
    else:
      self.drop_down_prescription_id_value.include_placeholder = False
      _ids = entity_id_to_fields.keys()
      self.drop_down_prescription_id_value.items = sorted( \
        [(entity_id_to_fields[_id]['prescription_display_name'], _id) for _id in _ids], key = lambda x: x[0])
      self.drop_down_prescription_id_value.selected_value = self.drop_down_prescription_id_value.items[0][1]
    
    self.validator.require(self.drop_down_prescription_id_value,
                      ['change'],
                      lambda dd: bool(dd.items),
                      self.label_prescription_id_value_invalid
                          )
 
    if initial_doctor_id != "":
      url = f'{self.router.base_url}appointment-available-date-and-times/{initial_doctor_id}'
      try:
        date_and_times = self.http.request(url, method='GET', json=True)
      except anvil.http.HttpError as e:
        self.label_validation_errors.text += self.http.get_error_message(e) 
      self.drop_down_date_and_time_value.include_placeholder = False
      self.drop_down_date_and_time_value.items = sorted([(dt,dt) for dt in date_and_times], key = lambda x: x[0])
      self.drop_down_date_and_time_value.selected_value = self.drop_down_date_and_time_value.items[0][1]
    else:
      self.drop_down_date_and_time_value.include_placeholder = True
      self.drop_down_date_and_time_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_date_and_time_value.items = []

    self.validator.require(self.drop_down_date_and_time_value,
                      ['change'],
                      lambda dd: bool(dd.items),
                      self.label_date_and_time_value_invalid
                          )
    
    self.text_area_comments_value.text = ""
    
    self.validator.enable_when_valid(self.button_submit)
    self.validator.show_all_errors()