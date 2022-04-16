import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import requests

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
FAST_API_BACKEND_BASE_URL = r'https://wic-backend.herokuapp.com/'

def base_request(url, method="GET", data=None, json=False, headers=None):
  params = {'url': url, 'method': method}
  
  if data is not None:
    params['data']=data
    
  if headers is not None:
    params['headers'] = headers
  
  resp = requests.request(**params)
  
  if json:
    return resp.json()
  
  return resp

@anvil.server.callable
def auth_request(*args, **kwargs):
  token = anvil.server.session["token"]
  headers = {'Authorization': f"Bearer {token}"}
  
  auth_args = {**kwargs, 'headers': headers}
  
  return base_request(*args, **auth_args)

@anvil.server.callable
def login(username, password):
  result = base_request(f"{FAST_API_BACKEND_BASE_URL}auth/jwt/login", "POST", {'username': username, 'password': password}, json=False)
  
  if result.ok:
    token = result.json()['access_token']
    anvil.server.session['token'] = token
    # TODO add expiration date from token to automatically log out.
    
    return
  
  raise anvil.http.HttpError(status=result.status_code, content=result.content)
    
  
