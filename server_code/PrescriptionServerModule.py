import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def set_prescriptions(prescriptions):
  anvil.server.session["session_prescriptions"] = prescriptions
  print(prescriptions)
  
@anvil.server.callable
def get_prescriptions():
  return anvil.server.session.get("session_prescriptions")
  
@anvil.server.callable
def set_selected_prescription_id(prescription_id):
  if prescription_id != None:
    anvil.server.session["selected_prescription_id"] = prescription_id

@anvil.server.callable
def get_selected_prescription():
  selected_prescription_id = anvil.server.session.get("selected_prescription_id")
  session_prescriptions = anvil.server.session.get("session_prescriptions")
  selected_prescription = next((x for x in session_prescriptions if x["id"] == selected_prescription_id))
  return selected_prescription

