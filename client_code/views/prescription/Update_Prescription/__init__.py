from ._anvil_designer import Update_PrescriptionTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'prescription'

class Update_Prescription(Update_PrescriptionTemplate):
  def __init__(self, router, validator, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    self.validator = validator
    self.validator.require(self.text_box_medication_value,
                           ['change'],
                           lambda tb: 2 <= len(tb.text) <= 100,
                           self.label_medication_value_invalid
                          )
    self.validator.require(self.text_box_quantity_value,
                           ['change'],
                           lambda tb: tb.text.isnumeric() and  
                                      float(tb.text) > 0 and
                                      tb.text != '',
                           self.label_quantity_value_invalid
                          )
    self.validator.enable_when_valid(self.button_submit)      
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use PUT request to web api
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'

    data_dict = { \
      'medication': self.text_box_medication_value.text,
      'quantity': self.text_box_quantity_value.text,
      'unit_id': self.drop_down_unit_id_value.selected_value
    }
    
    try:
      resp = anvil.http.request(url, method='PUT', data=data_dict, json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'

  def form_show(self, **event_args):
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}-with-id-display-name/{current_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    self.label_validation_errors.text = ""    
    self.label_id_value.text = current_id
    self.text_box_medication_value.text = current_entity_id_to_fields[current_id]['medication']
    self.text_box_quantity_value.text = current_entity_id_to_fields[current_id]['quantity']
    
    # use GET requests for list units
    # to populate all of the drop down(s)
    url = f'{self.router.base_url}units'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    _ids = entity_id_to_fields.keys()
    self.drop_down_unit_id_value.items = sorted(\
      [(entity_id_to_fields[_id]['name'], _id) for _id in _ids], key = lambda x: x[0])
    
    self.drop_down_unit_id_value.selected_value = str(current_entity_id_to_fields[current_id]['unit_id'])
    
    self.validator.show_all_errors()