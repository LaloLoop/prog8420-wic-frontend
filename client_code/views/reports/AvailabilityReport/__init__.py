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
    self.av_grid.role = 'wide'

    # Any code you write here will run when the form opens.

  def gen_report_click(self, **event_args):
    """This method is called when the button is clicked"""
    data = anvil.http.request(f"{self.router.base_url}reports/availability", json=True)
    
    columns = data['columns']
    report_data = data['data']
    first_col_width = 200
    col_width = 100
    
    column_names = ['Doctor'] + [s[s.index('T') + 1:-3] for s in columns[1:]]
    
    grid_cols=[{'id':col,
                'width': first_col_width if i == 0 else col_width, 
                'title':title,
                'data_key':col} for i, (title, col) in enumerate(zip(column_names, columns))]
    
    self.av_grid.rows_per_page = 10
    self.av_grid.show_page_controls = True
    #self.av_grid.width = col_width * len(grid_cols)
    self.av_grid.columns = grid_cols
    self.repeating_panel_1.items = report_data
    

  def nav_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.router.nav_to_route_view(self, 'home', 'admin')

  def av_grid_show(self, **event_args):
    """This method is called when the data grid is shown on the screen"""
    self.gen_report_click()




  