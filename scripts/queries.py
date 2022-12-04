
from . import db


@db.execute(fetch="one")
def select_now():
  return "SELECT NOW() as now"


@db.execute(fetch="all")
def select_recorded_months():
  return "SELECT DISTINCT date_recorded FROM fmc.retr"


@db.execute(fetch="all")
def select_conveyance_codes():
  return "SELECT * FROM fmc.retr_conveyance_code"

