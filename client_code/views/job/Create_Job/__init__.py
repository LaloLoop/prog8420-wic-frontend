from ._anvil_designer import Create_JobTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'job'

class Create_Job(Create_JobTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
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
    
    successful_request = False
    try:
      resp = anvil.http.request(url, method='POST', data=data_dict, json=True)
      successful_request = True
    except: # 404 error, this is a main.py endpoint error, not schemas.py ValidationError
      resp = {'detail': 'Job already exists?.'}

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