from ._anvil_designer import Update_JobTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from form_checker import validation

model_name = 'job'

class Update_Job(Update_JobTemplate):
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
    self.drop_down_date_and_time.items = [(dt,dt) for dt in resp]
    self.refresh_data_bindings()
    
  def button_submit_click(self, **event_args):
    # use PUT request to web api
    url = f'{self.router.base_url}{model_name}/{self.label_id_value.text}'
    
    data_dict = {
      'title': self.label_title_value.text,
      'speciality': self.text_box_speciality_value.text,
    }

    try:
      resp = anvil.http.request(url, method='PUT', data=data_dict, json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'

  def form_show(self, **event_args):
    current_id = anvil.server.call('get_selected_entity_id')
    
    url = f"{self.router.base_url}{model_name}/{current_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    current_entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)

    self.label_validation_errors.text = ""    
    self.label_id_value.text = current_id
    
    # use GET requests for list of job titles
    # to populate all of the drop downs
    url = f'{self.router.base_url}{model_name}-list-of-job-titles'
    job_titles = anvil.http.request(url, method='GET', json=True)
    
    self.label_title_value.text = current_entity_id_to_fields[current_id]['title']
    self.text_box_speciality_value.text = current_entity_id_to_fields[current_id]['speciality']
