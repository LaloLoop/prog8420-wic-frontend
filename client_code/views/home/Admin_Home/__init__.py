from ._anvil_designer import Admin_HomeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Admin_Home(Admin_HomeTemplate):
  def __init__(self, router=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.router = router
    # Any code you write here will run when the form opens.

  def button_crud_person_click(self, **event_args):
    self.router.nav_to_route_view(self, 'person', 'crud')

  def button_crud_job_click(self, **event_args):
    self.router.nav_to_route_view(self, 'job', 'crud')

  def button_crud_employee_click(self, **event_args):
    self.router.nav_to_route_view(self, 'employee', 'crud')

  def button_crud_patient_click(self, **event_args):
    self.router.nav_to_route_view(self, 'patient', 'crud')

  def button_crud_unit_click(self, **event_args):
    self.router.nav_to_route_view(self, 'unit', 'crud')

  def button_crud_prescription_click(self, **event_args):
    self.router.nav_to_route_view(self, 'prescription', 'crud')

  def button_crud_appointment_click(self, **event_args):
    self.router.nav_to_route_view(self, 'appointment', 'crud')

  def button_reports_click(self, **event_args):
    pass
  
  def button_logout_click(self, **event_args):
    self.router.nav_to_route_view(self, 'home', 'staff') # cycle through all 3














