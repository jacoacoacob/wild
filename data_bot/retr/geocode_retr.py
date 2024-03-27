import os

from ..lib import job, db

@db.query(fetch="all")
def query_distinct_addresses():
  sql_file_path = "queries/select_distinct_addresses.sql"
  with open(os.path.abspath(sql_file_path), "r") as sql_file:
    return sql_file.read()

class GeocodeRetr(job.Job):
  def __init__(self, rerun_job_id=None, verbose=0) -> None:
    super().__init__(rerun_job_id, verbose)

  def execute(self, *args, **kwargs):
    self.stage_one()

  @job.stage
  def stage_one(self):
    addresses = query_distinct_addresses()
    print(len(addresses))
