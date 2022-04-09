import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

from . import router as r

r.get_crud_view_shower('job').show_view('crud'/'read/')

def say_hello():
  print("Hello, world")
