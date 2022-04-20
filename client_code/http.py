import anvil.server
import anvil.users
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

class HttpClient:
  def __init__(self, base_url):
    self.base_url = base_url
  
  def request(self, *args, **kwargs):
    resp = anvil.server.call('auth_request', *args, **kwargs)
    if not resp['ok']:
      raise anvil.http.HttpError(resp['status_code'], resp['content'])
      
    return resp['content']
  
  def login(self, username, password):
    result = anvil.server.call("login", f"{self.base_url}", username, password)
    
    if not result['ok']:
      status_code = result['status_code']
      if status_code >= 400 and status_code < 500:
        msg = "Check your credentials"
      elif status_code >= 500:
        msg = "We had problems trying to log you in, please try again later"
      else:
        msg = "Unknown error"
      
      raise anvil.http.HttpError(status_code, msg)
    
    return result['content']

  
  def is_logged_in(self):
    return anvil.server.call('is_logged_in', self.base_url)
  
      
  def get_error_message(self, e: anvil.Http.Error):
    error_message =""
    if e.status == 500:
      error_message = f'Couldn''t perfom CRUD operation on backend; perhaps another entity depends on this entity.'
    elif e.status == 422: # back end validation errors 
      for v_err in e.content['detail']:
        error_message += f"{v_err['loc'][1]}: {v_err['msg']}\n"
    else:
      error_message = f'{e.status}\n{e.content}'
    return error_message + '\n'
  
