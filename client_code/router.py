import anvil
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .views.Base import Base

from .views.auth.LoginForm import LoginForm
from .views.home.Admin_Home import Admin_Home
from .views.home.Staff_Home import Staff_Home
from .views.home.Doctor_Home import Doctor_Home
from .views.person.CRUD_Person import CRUD_Person
from .views.person.Create_Person import Create_Person
from .views.person.Read_Person import Read_Person
from .views.person.Update_Person import Update_Person
from .views.person.Delete_Person import Delete_Person
from .views.job.CRUD_Job import CRUD_Job
from .views.job.Create_Job import Create_Job
from .views.job.Read_Job import Read_Job
from .views.job.Update_Job import Update_Job
from .views.job.Delete_Job import Delete_Job
from .views.employee.CRUD_Employee import CRUD_Employee
from .views.employee.Create_Employee import Create_Employee
from .views.employee.Read_Employee import Read_Employee
from .views.employee.Update_Employee import Update_Employee
from .views.employee.Delete_Employee import Delete_Employee
from .views.patient.CRUD_Patient import CRUD_Patient
from .views.patient.Create_Patient import Create_Patient
from .views.patient.Read_Patient import Read_Patient
from .views.patient.Update_Patient import Update_Patient
from .views.patient.Delete_Patient import Delete_Patient
from .views.unit.CRUD_Unit import CRUD_Unit
from .views.unit.Create_Unit import Create_Unit
from .views.unit.Read_Unit import Read_Unit
from .views.unit.Update_Unit import Update_Unit
from .views.unit.Delete_Unit import Delete_Unit
from .views.prescription.CRUD_Prescription import CRUD_Prescription
from .views.prescription.Create_Prescription import Create_Prescription
from .views.prescription.Read_Prescription import Read_Prescription
from .views.prescription.Update_Prescription import Update_Prescription
from .views.prescription.Delete_Prescription import Delete_Prescription
from .views.appointment.CRUD_Appointment import CRUD_Appointment
from .views.appointment.Create_Appointment import Create_Appointment
from .views.appointment.Read_Appointment import Read_Appointment
from .views.appointment.Update_Appointment import Update_Appointment
from .views.appointment.Delete_Appointment import Delete_Appointment

FAST_API_BACKEND_BASE_URL = r'https://wic-backend.herokuapp.com/'

class Router:
  base_url = FAST_API_BACKEND_BASE_URL # use this for GET/POST/PUT/DELETE in f-string
  crud_dropdown_placeholder = "None"
  
  def nav_to_route_view(old_form, route:str, view:str):
      old_form.remove_from_parent()
      anvil.get_open_form().content_panel.add_component(routes[route][view])
      
  def convert_resp_to_entity_id_to_fields_dict(resp):
    if not isinstance(resp, list): # if response is a single dict, vs list of dicts
      resp = [resp] 
    
    entity_id_to_fields = {}
    for e in resp:
      e_id = e['id']
      del e['id']
      entity_id_to_fields[str(e_id)] = {**e}
    return entity_id_to_fields
  
auth_views = {
  'login': LoginForm(router=Router)
}
  
home_views = {
              'admin':Admin_Home(router=Router),
              'staff':Staff_Home(router=Router),
              'doctor': Doctor_Home(router=Router)
             }

person_views = {
                'crud':CRUD_Person(router=Router),
                'create':Create_Person(router=Router),
                'read':Read_Person(router=Router),
                'update':Update_Person(router=Router),
                'delete':Delete_Person(router=Router)
                }

job_views = {
             'crud':CRUD_Job(router=Router),
             'create':Create_Job(router=Router),
             'read':Read_Job(router=Router),
             'update':Update_Job(router=Router),
             'delete':Delete_Job(router=Router),
            }

employee_views = {
                  'crud':CRUD_Employee(router=Router),
                  'create': Create_Employee(router=Router),
                  'read': Read_Employee(router=Router),
                  'update':Update_Employee(router=Router),
                  'delete':Delete_Employee(router=Router),
                  }

patient_views = {
                 'crud':CRUD_Patient(router=Router),
                 'create':Create_Patient(router=Router),
                 'read':Read_Patient(router=Router),
                 'update':Update_Patient(router=Router),
                 'delete':Delete_Patient(router=Router),
                }

unit_views = {
              'crud':CRUD_Unit(router=Router),
              'create': Create_Unit(router=Router),
              'read':Read_Unit(router=Router),
              'update':Update_Unit(router=Router),
              'delete':Delete_Unit(router=Router),
              }

prescription_views = {
                      'crud':CRUD_Prescription(router=Router),
                      'create':Create_Prescription(router=Router),
                      'read':Read_Prescription(router=Router),
                      'update':Update_Prescription(router=Router),
                      'delete':Delete_Prescription(router=Router),
                      }

appointment_views = {
                     'crud':CRUD_Appointment(router=Router),
                     'create':Create_Appointment(router=Router),
                     'read':Read_Appointment(router=Router),
                     'update':Update_Appointment(router=Router),
                     'delete':Delete_Appointment(router=Router),
                    }

report_views = {}

routes = {
  'auth': auth_views,
  'home': home_views,
  'person': person_views,
  'job': job_views,
  'employee': employee_views,
  'patient': patient_views,
  'unit': unit_views,
  'prescription': prescription_views,
  'appointment': appointment_views,
  'report': report_views,
}

# since router is our startup module, open the Base Form here
base = Base(router=Router)
anvil.open_form(base)
