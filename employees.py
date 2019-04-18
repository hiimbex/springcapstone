import random
from keymaker import *

class Employee:
  def __init__(self):
    self.id = random.randint(10000, 99999)
    self.key = MasterKey()

  def get_key(self):
    return self.key

  def get_id(self):
    return self.id
