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

@anvil.server.callable
def base_request(url, method="GET", data=None, headers=None):
  params = {'url': url, 'method': method}
  
  if data is not None:
    params['data']=data
    
  if headers is not None:
    params['headers'] = headers
  
  resp = requests.request(**params)
  
  return resp

@anvil.server.callable
def request(*args, json=True, **kwargs):
  resp = base_request(*args, **kwargs)
  
  if json:
    content = resp.json()
  else:
    content = resp.content
  
  return {'status_code': resp.status_code, 'content': content, 'ok': resp.ok}

@anvil.server.callable
def auth_request(*args, **kwargs):
  # TODO add expiration date from token to automatically log out.
  token = anvil.server.session["token"]
  headers = {'Authorization': f"Bearer {token}"}
  
  auth_args = {**kwargs, 'headers': headers}
  
  return request(*args, **auth_args)

class FlowStep:
  def __init__(self, base_url):
    self.base_url = base_url
    
  def request(self, *args, **kwargs):
    raise NotImplementedError("base request method called")
    
  def process_response(self, response):
    raise NotImplementedError("base process_response called")
  
  def run(self, *args, **kwargs):
    resp = self.request(*args, **kwargs)
    if not resp['ok']:
      return resp
    
    proc_res = self.process_response(resp)
    
    return resp if proc_res is None else proc_res

class LoginStep(FlowStep):
  def request(self, *args, **kwargs):
    username = args[0]
    password = args[1]
    return request(f"{self.base_url}auth/jwt/login", "POST", 
                   {'username': username, 'password': password})
  
  def process_response(self, response):
    if response['ok']:
      token = response['content']['access_token']
      anvil.server.session['token'] = token

class GetUserStep(FlowStep):
  def request(self, *args, **kwargs):
    return auth_request(f"{self.base_url}users/me")
  
  def process_response(self, response):
    if response['ok']:
      user = response['content']
      anvil.server.session['user_info'] = user

class GetJobTitle(FlowStep):
  def request(self, *args, **kwargs):
    user_info = anvil.server.session.get('user_info')
    
    return auth_request(f"{self.base_url}job/{user_info['job_id']}")
  
  def process_response(self, response):
    if response['ok']:
      job = response['content']
      anvil.server.session['job_title'] = job
      
@anvil.server.callable
def login(base_url, username, password):
    steps = [LoginStep(base_url), GetUserStep(base_url), GetJobTitle(base_url)]
    
    final_resp = None
    for s in steps:
      final_resp = s.run(username, password)
      if not final_resp['ok']:
        break
        
    return final_resp
  
@anvil.server.callable
def get_session_permissions():
  return anvil.server.session['job_title']['title']
  

@anvil.server.callable
def logout(base_url):
  resp = request(f"{base_url}auth/jwt/logout", "POST")
  
  del anvil.server.session['token']
  del anvil.server.session['user_info']
  del anvil.server.session['job_title']
  
  return resp

@anvil.server.callable
def is_logged_in(base_url):
  token = anvil.server.session.get('token')
  if token is not None:
    resp = GetUserStep(base_url).run()
    return resp['ok']
  
  return False