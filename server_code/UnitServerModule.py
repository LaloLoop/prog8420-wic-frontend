import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def set_units(units):
  anvil.server.session["session_units"] = units
  print(units)
  
@anvil.server.callable
def get_units():
  return anvil.server.session.get("session_units")
  
@anvil.server.callable
def set_selected_unit_id(unit_id):
  anvil.server.session["selected_unit_id"] = unit_id

@anvil.server.callable
def get_selected_unit():
  selected_unit_id = anvil.server.session.get("selected_unit_id")
  session_units = anvil.server.session.get("session_units")
  selected_unit = next((x for x in session_units if x["id"] == selected_unit_id))
  return selected_unit

