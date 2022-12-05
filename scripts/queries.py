
from .lib import execute


@execute(fetch="one")
def select_now(*args, **kwargs):
  print(kwargs)
  return "SELECT NOW() as now"


@execute(fetch="all")
def select_recorded_months(*args, **kwargs):
  return "SELECT DISTINCT date_recorded FROM fmc.retr"


@execute(fetch="all")
def select_conveyance_codes(*args, **kwargs):
  return "SELECT * FROM fmc.retr_conveyance_code"

