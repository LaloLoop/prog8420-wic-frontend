from ._anvil_designer import Create_JobTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'job'

class Create_Job(Create_JobTemplate):
  def __init__(self, router, httpc, validator, **properties):
    self.init_components(**properties)
    self.router = router
    self.http = httpc
    self.validator = validator
    self.validator.require(self.text_box_speciality_value,
                           ['change','lost_focus'],
                           lambda tb: 0 < len(tb.text) <= 50,
                           self.label_speciality_value_invalid
                          )
    
    self.validator.enable_when_valid(self.button_submit)
    
    self.validator.show_all_errors()

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')
    
  def button_submit_click(self, **event_args):
    self.label_validation_errors.text = ""
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}/'

    data_dict = { \
      'title': self.drop_down_title_value.selected_value,
      'speciality': self.text_box_speciality_value.text,
    }
    
    try:
      resp = self.http.request(url, method='POST', data=data_dict, json=True)
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)  

  def form_show(self, **event_args):
    self.label_validation_errors.text = ""
    # use GET requests for list of job titles
    # to populate all of the drop downs
    url = f'{self.router.base_url}{model_name}-list-of-job-titles'
    try:
      job_titles = self.http.request(url, method='GET', json=True)
    except anvil.http.HttpError as e:
      self.label_validation_errors.text += self.http.get_error_message(e)  

    self.drop_down_title_value.items = sorted([(jt,jt) for jt in job_titles], key = lambda x: x[0])
   
    self.drop_down_title_value.selected_value =  self.drop_down_title_value.items[0][1]  
        
    self.text_box_speciality_value.text = ""
    
    self.validator.show_all_errors()