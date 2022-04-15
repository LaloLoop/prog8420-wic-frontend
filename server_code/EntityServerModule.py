import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def set_selected_entity_id(entity_id):
  if entity_id != None:
    anvil.server.session["selected_entity_id"] = entity_id

@anvil.server.callable
def get_selected_entity_id():
  return anvil.server.session['selected_entity_id']
