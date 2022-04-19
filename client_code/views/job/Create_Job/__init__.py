from ._anvil_designer import Create_JobTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'job'

class Create_Job(Create_JobTemplate):
  def __init__(self, router, validator, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    self.validator = validator
    self.validator.require(self.text_box_name_value,
                           ['change','lost_focus'],
                           lambda tb: 2 <= len(tb.text) <= 100,
                           self.label_name_value_invalid
                          )
    # TODO: allow adding new/different specialties 
    @validator('speciality')
    def speciality_must_be_no_more_than_50_characters(cls, v):
        if len(v) > 50:
            raise ValueError(f'{v} must be no more than 50 characters')
        return     
    self.validator.enable_when_valid(self.button_submit)
    
    self.validator.show_all_errors()
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')
    
  def button_submit_click(self, **event_args):
    # use POST request to web api
    url = f'{self.router.base_url}{model_name}/'

    data_dict = { \
      'title': self.drop_down_title_value.selected_value,
      'speciality': self.text_box_speciality_value.text,
    }
    
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      self.label_validation_errors.text = ''
      self.router.nav_to_route_view(self, model_name, 'crud')
    except anvil.http.HttpError as e:
      self.label_validation_errors.text = f'{e.status}'

  def form_show(self, **event_args):
    # use GET requests for list of job titles
    # to populate all of the drop downs
    url = f'{self.router.base_url}{model_name}-list-of-job-titles'
    job_titles = anvil.http.request(url, method='GET', json=True)

    self.label_validation_errors.text = ""
    
    self.drop_down_title_value.include_placeholder = True
    self.drop_down_title_value.placeholder = self.router.crud_dropdown_placeholder
    self.drop_down_title_value.selected_value = self.router.crud_dropdown_placeholder    
    
    self.drop_down_title_value.items = sorted([(jt,jt) for jt in job_titles], key = lambda x: x[0])
    
    self.text_box_speciality_value.text = ""