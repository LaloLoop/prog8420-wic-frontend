from ._anvil_designer import AvailabilityReportTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AvailabilityReport(AvailabilityReportTemplate):
  def __init__(self, router, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router

    # Any code you write here will run when the form opens.

  def gen_report_click(self, **event_args):
    """This method is called when the button is clicked"""
    data = anvil.http.request(f"{self.router.base_url}reports/availability", json=True)
    
    self.text_area_1.text = data


  