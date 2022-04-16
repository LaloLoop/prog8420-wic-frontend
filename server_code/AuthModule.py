import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import requests
from .router import FAST_API_BACKEND_BASE_URL

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
def wic_request(url, method="GET", data=None, json=False):
  params = {'url': url, 'method': method}
  if data is not None:
    params['data']=data
  
  resp = requests.request(**params)
  
  if json:
    return resp.json()
  
  return resp

def login(username, password):
  result = wic_request(f"{FAST_API_BACKEND_BASE_URL}auth/jwt/login", "POST", {'username': username, 'password': password}, json=True)
  
  if result.ok:
    token = result.json()['access_token']
    anvil.server.session['token'] = token
    # TODO add expiration date from token to automatically log out.
  
  
