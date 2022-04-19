from ._anvil_designer import Create_PatientTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'patient'

class Create_Patient(Create_PatientTemplate):
  def __init__(self, router, validator, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    self.validator = validator
    # do self.validator.require(drop_down_person_id_value) only at form_show, to avoid None
    self.validator.require(self.text_box_ohip_value,
                           ['change','lost_focus'],
                           lambda tb: self.validator.check_valid_ohip_number(tb.text),
                           self.label_ohip_value_invalid
                           )
    self.validator.enable_when_valid(self.button_submit)    
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def button_submit_click(self, **event_args):
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}/'

    data_dict = {
      'person_id': self.drop_down_person_id_value.selected_value,
      'ohip': self.text_box_ohip_value.text
    }
    
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'

  def form_show(self, **event_args):
    # use GET requests for list of unassigned persons
    # to populate all of the drop downs
    url = f'{self.router.base_url}persons-unassigned'
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    self.label_validation_errors.text = ""
    
    if not entity_id_to_fields:
      self.drop_down_person_id_value.include_placeholder = True
      self.drop_down_person_id_value.placeholder = self.router.crud_dropdown_placeholder
      self.drop_down_person_id_value.items = []
    else:
      self.drop_down_person_id_value.include_placeholder = False
      _ids = entity_id_to_fields.keys()
      self.drop_down_person_id_value.items = sorted( \
        [(entity_id_to_fields[_id]['email'], _id) for _id in _ids], key = lambda x: x[0])
      self.drop_down_person_id_value.selected_value = self.drop_down_person_id_value.items[0][1]
    
    self.validator.require(self.drop_down_person_id_value,
                      ['change'],
                      lambda dd: bool(dd.items),
                      self.label_person_id_value_invalid
                      )
    
    self.text_box_ohip_value.text = ""
    self.validator.show_all_errors()