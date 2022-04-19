import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import re
from datetime import date, timedelta
from datetime import datetime

class Validator():
  """
A Validator instance performs form validation. You give it
a set of components, and for each component you specify
a checking function (a predicate), and optionally an error
label that will be shown if the component is *not* valid.

It will show error labels when the component is not valid

Add components to it with the require() method. Eg:

  validator.require(self.text_box_1, ['change', 'lost_focus'],
                    lambda tb: tb.text != '',
                    self.error_lbl_1)
                    
It also has some utility functions for common requirements
such as "this text box must have text in it", or
"this checkbox must be checked".

Use the enable_when_valid() method to provide a component
that will be enabled (via its `enable` property) only when
all requirements are met. Or just use the is_valid() method
to check the status of the form.

  validator.enable_when_valid(self.submit_button)

  """
  def __init__(self):
    self._validity = {}
    self._actions = []
    self._component_checks = []
    
  def require(self, component, event_list, predicate, error_lbl=None, show_errors_immediately=False):
    def check_this_component(**e):
      result = predicate(component)
      self._validity[component] = result
      if error_lbl is not None:
        error_lbl.visible = not result
      self._check()
      
    for e in event_list:
      component.set_event_handler(e, check_this_component)
    self._component_checks.append(check_this_component)
      
    if show_errors_immediately:
      check_this_component()
    else:
      # By default, won't show the error until the event triggers,
      # but we will (eg) disable buttons
      if error_lbl is not None:
        error_lbl.visible = False
      self._validity[component] = predicate(component)
      self._check()
   
  def require_text_field(self, text_box, error_lbl=None, show_errors_immediately=False):
    self.require(text_box, ['change', 'lost_focus'],
                 lambda tb: tb.text != '',
                 error_lbl, show_errors_immediately)
        
  def require_checked(self, check_box, error_lbl=None, show_errors_immediately=False):
    self.require(check_box, ['change'],
                 lambda cb: cb.checked,
                 error_lbl, show_errors_immediately)
      
  def enable_when_valid(self, component):
    def on_change(is_valid):
      component.enabled = is_valid
    self._actions.append(on_change)
    self._check()

  def is_valid(self):
    """Return True if this form is valid, False if it's not"""
    return all(self._validity.values())
  
  def show_all_errors(self):
    """Show all error labels, even if the """
    for check_component in self._component_checks:
      check_component()
    
  def _check(self):
    v = self.is_valid()
    for f in self._actions:
      f(v)

  # validations for forms  
  def check_valid_first_or_last_name(self, value):
    return 2 <= len(value) <= 100 and re.match(r"^[a-zA-Z ]*$", value)

  def check_valid_birthdate(self, value: date):
    return (date.today() - timedelta(days=150*365)) < value < date.today()
  
  def check_valid_street_or_city(self, value):
    return 2 <= len(value) <= 100 and re.match(r"^[a-zA-Z0-9. ]*$", value)
  
  # https://www.c-sharpcorner.com/article/how-to-validate-an-email-address-in-python/
  def check_valid_email(self, email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    return re.search(regex ,email)
        
  # taken from https://stackoverflow.com/a/47802790
  def check_valid_canadian_postalcode(self, p, strictCapitalization=False, fixSpace=False):
    '''By default lower and upper case characters are allowed,  
    a missing middle space will be substituted.'''

    pc = p.strip()                   # copy p, strip whitespaces front/end
    if fixSpace and len(pc) == 6:
        pc = pc[0:3] + " " + pc[3:]    # if allowed / needed insert missing space

    nums = "0123456789"              # allowed numbers
    alph = "ABCEGHJKLMNPRSTVWXYZ"    # allowed characters (WZ handled below)
    mustBeNums = [1,4,6]             # index of number
    mustBeAlph = [0,2,5]             # index of character (WZ handled below)

    illegalCharacters = [x for x in pc 
                        if x not in (nums + alph.lower() + alph + " ")]

    if strictCapitalization:
        illegalCharacters = [x for x in pc
                            if x not in (alph + nums + " ")]

    if illegalCharacters:
        return False #(False, "Illegal characters detected: " + str(illegalCharacters))

    postalCode = [x.upper() for x in pc]          # copy to uppercase list

    if len(postalCode) != 7:                      # length-validation
        return False #(False, "Length not 7")

    for idx in range(0,len(postalCode)):          # loop over all indexes
        ch = postalCode[idx]
        if ch in nums and idx not in mustBeNums:  # is is number, check index
            return False #(False, "Format not 'ADA DAD'")     
        elif ch in alph and idx not in mustBeAlph: # id is character, check index
            return False #(False, "Format not 'ADA DAD'") # alpha / digit
        elif ch == " " and idx != 3:               # is space in between
            return False #(False, "Format not 'ADA DAD'")

    if postalCode[0] in "WZ":                      # no W or Z first char
        return False #(False, "Cant start with W or Z")

    return True # (True,"".join(postalCode))    # yep - all good

  def check_valid_phonenumber(self, value):
    num_digits_found = 0
    
    for char in value:
        if char.isdigit():
            num_digits_found += 1
            if num_digits_found == 7:
                return True
        
    if num_digits_found < 7:
        return False
    return True
  
  def check_valid_ohip_number(self, value):
    if len(value) != 12:
        return False
    elif not value[0:9].isdigit() or not value[-2:].isalpha():
        return False
    return True