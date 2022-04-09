import anvil
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .views._home.Admin_Home import Admin_Home
from .views._home.Staff_Home import Staff_Home
from .views._home.Doctor_Home import Doctor_Home
from .views.x.CRUD_q import CRUD_q
from .views.x.Create_q import Create_q
from .views.x.Read_q import Read_q
from .views.x.Update_q import Update_q
from .views.x.Delete_q import Delete_q
#from .views.job import 
#from .views.employee import
#from .views.patient import
#from .views.prescription import
#from .views.unit import
#from .views.appointment import

home_forms_dict = {'admin':Admin_Home(), 'staff':Staff_Home(), 'doctor': Doctor_Home()}

def show_home_view(old_form, job_title:str, after_login:bool = False):
  if not after_login:
    old_form.remove_from_parent()
  anvil.get_open_form().content_panel.add_component(home_forms_dict[job_title])

person_crud_form_dict = {'crud':CRUD_Person(),'create':Create_Person(),'read':Read_Person(),'update':Update_Person(),'delete':Delete_Person()}
#job_crud_form_dict = {'crud':CRUD_Job(),'create':Create_Job()),'read':Read_Job(),'update':Update_Job(),'delete':Delete_Job()}
#employee_crud_form_dict = {'crud':CRUD_Employee(),'create': Create_Employee()),'read': Read_Employee(),'update':Update_Employee(),'delete':Delete_Employee()}
#patient_crud_form_dict = {'crud':CRUD_Patient(),'create':Create_Patient()),'read':Read_Patient(),'update':Update_Patient(),'delete':Delete_Patient()}
#unit_crud_form_dict = {'crud':CRUD_Unit(),'create': Create_Unit()),'read':Read_Unit(),'update':Update_Unit(),'delete':Delete_Unit()}
#prescription_crud_form_dict = {'crud':CRUD_Prescription(),'create':Create_Prescription()),'read':Read_Prescription(),'update':Update_Prescription(),'delete':Delete_Prescription()}
#appointment_crud_form_dict = {'crud':CRUD_Appointment(),'create':Create_Appointment()),'read':Read_Appointment(),'update':Update_Appointment(),'delete':Delete_Appointment()}

def CRUD_View_Shower():
  def __init__(self, form_dict): # {'crud'}
    self.crud_form_dict = form_dict
  
  def show_view(self, view_name:str, old_form): # old_form should be self in the button callback
      old_form.remove_from_parent()
      anvil.get_open_form().content_panel.add_component(self.crud_form_dict['view_name'])

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