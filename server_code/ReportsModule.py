import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import pandas as pd

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def availabillity_schedule(base_url):
  url = f"{base_url}appointments-with-id-display-name/?skip=0&limit=1000"
  resp = requests.get(URL, json=True)
  appointments_json = resp.json()
  
  appointments_df = pd.DataFrame.from_dict(appointments_json)
  
  appt_by_doctor_by_time = appointments_df.groupby(["doctor_display_name", "date_and_time"]).agg({'patient_id': "count"}).reset_index()
  availability_pivot = appt_by_doctor_by_time.pivot_table('patient_id', ['doctor_display_name'], 'date_and_time')
  
  schedules = available_schedules.replace(np.nan, 'Available')
  schedules = schedules.replace(1.0, 'Busy')
  
  return schedules.to_json()