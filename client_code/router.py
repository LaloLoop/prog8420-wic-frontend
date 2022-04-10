import anvil
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .views._home.Admin_Home import Admin_Home
from .views._home.Staff_Home import Staff_Home
from .views._home.Doctor_Home import Doctor_Home
from .views.person.CRUD_Person import CRUD_Person
from .views.person.Create_Person import Create_Person
from .views.person.Read_Person import Read_Person
from .views.person.Update_Person import Update_Person
from .views.person.Delete_Person import Delete_Person
#from .views.job.CRUD_Job import CRUD_Job
#from .views.job.Create_Job import Create_Job
#from .views.job.Read_Job import Read_Job
#from .views.job.Update_Job import Update_Job
#from .views.job.Delete_Job import Delete_Job
#from .views.employee.CRUD_Employee import CRUD_Employee
#from .views.employee.Create_Employee import Create_Employee
#from .views.employee.Read_Employee import Read_Employee
#from .views.employee.Update_Employee import Update_Employee
#from .views.employee.Delete_Employee import Delete_Employee
#from .views.patient.CRUD_Patient import CRUD_Patient
#from .views.patient.Create_Patient import Create_Patient
#from .views.patient.Read_Patient import Read_Patient
#from .views.patient.Update_Patient import Update_Patient
#from .views.patient.Delete_Patient import Delete_Patient
#from .views.unit.CRUD_Unit import CRUD_Unit
#from .views.unit.Create_Unit import Create_Unit
#from .views.unit.Read_Unit import Read_Unit
#from .views.unit.Update_Unit import Update_Unit
#from .views.unit.Delete_Unit import Delete_Unit
#from .views.prescription.CRUD_Prescription import CRUD_Prescription
#from .views.prescription.Create_Prescription import Create_Prescription
#from .views.prescription.Read_Prescription import Read_Prescription
#from .views.prescription.Update_Prescription import Update_Prescription
#from .views.prescription.Delete_Prescription import Delete_Prescription
#from .views.appointment.CRUD_Appointment import CRUD_Appointment
#from .views.appointment.Create_Appointment import Create_Appointment
#from .views.appointment.Read_Appointment import Read_Appointment
#from .views.appointment.Update_Appointment import Update_Appointment
#from .views.appointment.Delete_Appointment import Delete_Appointmen

FAST_API_BACKEND_BASE_URL = 'http://localhost:8080/'

class Router:
  base_url = FAST_API_BACKEND_URL # use this for GET/POST/PUT/DELETE in f-string

  def nav_to_route_view(self, old_form, route:str, view:str):
      old_form.remove_from_parent()
      anvil.get_open_form().content_panel.add_component(routes[route][view])

home_views = {'admin':Admin_Home(router=Router()), 'staff':Staff_Home(router=Router), 'doctor': Doctor_Home(router=Router)}
person_views = { 'crud':CRUD_Person(),'create':Create_Person(),'read':Read_Person(),'update':Update_Person(),'delete':Delete_Person()}
job_views = {} # '#crud':CRUD_Job(),'create':Create_Job()),'read':Read_Job(),'update':Update_Job(),'delete':Delete_Job()}
employee_views = {} # 'crud':CRUD_Employee(),'create': Create_Employee()),'read': Read_Employee(),'update':Update_Employee(),'delete':Delete_Employee()}
patient_views = {} #'crud':CRUD_Patient(),'create':Create_Patient()),'read':Read_Patient(),'update':Update_Patient(),'delete':Delete_Patient()}
unit_views = {} #'crud':CRUD_Unit(),'create': Create_Unit()),'read':Read_Unit(),'update':Update_Unit(),'delete':Delete_Unit()}
prescription_views = {} #'crud':CRUD_Prescription(),'create':Create_Prescription()),'read':Read_Prescription(),'update':Update_Prescription(),'delete':Delete_Prescription()}
appointment_views = {} #'crud':CRUD_Appointment(),'create':Create_Appointment()),'read':Read_Appointment(),'update':Update_Appointment(),'delete':Delete_Appointment()}

routes = {
  'home': home_views,
  'person': person_views,
  'job': job_views,
  'employee': employee_views,
  'patient': patient_views,
  'unit': unit_views,
  'prescription': prescription_views,
  'appointment': appointment_views
}