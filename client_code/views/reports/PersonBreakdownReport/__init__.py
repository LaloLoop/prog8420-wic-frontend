from ._anvil_designer import PersonBreakdownReportTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from random import randint

class PersonBreakdownReport(PersonBreakdownReportTemplate):
  def __init__(self, router, **properties):
    self.init_components(**properties)
    self.router = router
    self.pb_grid.role = 'wide'

  def form_show(self, **event_args):
    self.pb_graph.source = f"{self.router.base_url}graphs/person-breakdown/{randint(0,100000)}" # fake random path param so we avoid a cached version
    
    data = anvil.http.request(f"{self.router.base_url}reports/person-breakdown", json=True)

    columns = data['columns']
    report_data = data['data']
    first_col_width = 200
    col_width = 100

    column_names = columns 

    grid_cols=[{'id':col,
                'width': first_col_width if i == 0 else col_width,
                'title':title,
                'data_key':col} for i, (title, col) in enumerate(zip(column_names, columns))]

    self.pb_grid.rows_per_page = 10
    self.pb_grid.show_page_controls = True
    #self.pb_grid.width = col_width * len(grid_cols)
    self.pb_grid.columns = grid_cols
    self.repeating_panel_1.items = report_data

  def nav_back_click(self, **event_args):
    self.router.nav_to_route_view(self, 'home', '')

  def pb_grid_show(self, **event_args):
    self.gen_report_click()

  def button_availability_report_click(self, **event_args):
    self.router.nav_to_route_view(self, 'report', 'availability')

  def button_timeslot_usage_click(self, **event_args):
    self.router.nav_to_route_view(self, 'report', 'timeslot_usage')

  def button_person_breakdown_click(self, **event_args):
    self.router.nav_to_route_view(self, 'report', 'person_breakdown')

  def button_entity_count_click(self, **event_args):
    self.router.nav_to_route_view(self, 'report', 'entity_count')

