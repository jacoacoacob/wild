
from .lib import query


@query(fetch="one")
def ping(*args, **kwargs):
  return "SELECT NOW() as now"


@query(fetch="all")
def select_recorded_months(*args, **kwargs):
  return "SELECT DISTINCT date_recorded FROM fmc.retr"


@query(fetch="all")
def select_conveyance_codes(*args, **kwargs):
  return "SELECT * FROM fmc.retr_conveyance_code"

