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

class Router:
    def show_home_view(old_form, job_title: str, after_login: bool = False):
        if not after_login:
            old_form.remove_from_parent()
        anvil.get_open_form().content_panel.add_component(home_forms_dict[job_title])

home_forms_dict = {'admin':Admin_Home(router=Router()), 'staff':Staff_Home(), 'doctor': Doctor_Home()}



person_crud_form_dict = {'crud':CRUD_Person(),'create':Create_Person(),'read':Read_Person(),'update':Update_Person(),'delete':Delete_Person()}
#job_crud_form_dict = {'crud':CRUD_Job(),'create':Create_Job()),'read':Read_Job(),'update':Update_Job(),'delete':Delete_Job()}
#employee_crud_form_dict = {'crud':CRUD_Employee(),'create': Create_Employee()),'read': Read_Employee(),'update':Update_Employee(),'delete':Delete_Employee()}
#patient_crud_form_dict = {'crud':CRUD_Patient(),'create':Create_Patient()),'read':Read_Patient(),'update':Update_Patient(),'delete':Delete_Patient()}
#unit_crud_form_dict = {'crud':CRUD_Unit(),'create': Create_Unit()),'read':Read_Unit(),'update':Update_Unit(),'delete':Delete_Unit()}
#prescription_crud_form_dict = {'crud':CRUD_Prescription(),'create':Create_Prescription()),'read':Read_Prescription(),'update':Update_Prescription(),'delete':Delete_Prescription()}
#appointment_crud_form_dict = {'crud':CRUD_Appointment(),'create':Create_Appointment()),'read':Read_Appointment(),'update':Update_Appointment(),'delete':Delete_Appointment()}

class CRUD_View_Shower:
  def __init__(self, form_dict): # {'crud'}
    self.crud_form_dict = form_dict
  
  def show_view(self, view_name:str, old_form): # old_form should be self in the button callback
      old_form.remove_from_parent()
      anvil.get_open_form().content_panel.add_component(self.crud_form_dict[view_name])

model_crud_view_showers_dict = {
  'person': CRUD_View_Shower(person_crud_form_dict),
# 'job'= CRUD_View_Shower(job_crud_form_dict),
# 'employee': CRUD_View_Shower(employee_crud_form_dict),
# 'patient': CRUD_View_Shower(patient_crud_form_dict),
# 'unit:' CRUD_View_Shower(unit_crud_form_dict),
# 'prescription': CRUD_View_Shower(prescription_crud_form_dict),
# 'appointment': CRUD_View_Shower(appointment_crud_form_dict)
}

def get_crud_view_shower(model_name):
  return model_crud_view_showers_dict[model_name]