from ._anvil_designer import Read_JobTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

model_name = 'job'

class Read_Job(Read_JobTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_back_click(self, **event_args):
    self.router.nav_to_route_view(self, model_name, 'crud')

  def form_show(self, **event_args):
    _id = anvil.server.call('get_selected_entity_id')
    url = f"{self.router.base_url}{model_name}/{_id}"
    resp = anvil.http.request(url, method='GET', json=True)
    entity_id_to_fields = self.router.convert_resp_to_entity_id_to_fields_dict(resp)
    
    # populate form with current values of entity
    self.label_id_value.text = _id
    self.label_title_value.text = entity_id_to_fields[_id]['title']
    self.label_speciality_value.text = entity_id_to_fields[_id]['speciality']



