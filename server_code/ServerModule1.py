import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:

# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
session_units = []
selected_unit_id = ""

@anvil.server.callable
def set_units(units):
  session_units = units
  print(session_units)
  
@anvil.server.callable
def get_units():
  return session_units
  
@anvil.server.callable
def set_selected_unit_id(unit_id):
  selected_unit_id = unit_id

@anvil.server.callable
def get_selected_unit():
  #selected_unit = next(x for x in session_units if x["id"] == selected_unit_id)
  return selected_unit_id
                       
