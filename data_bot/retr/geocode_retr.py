"""

"""

from ..lib import job, db


@db.query(fetch="one")
def query_addresses():
  return """
    WITH addresses AS (
      SELECT
        sale_number,
        TRIM(
          COALESCE(grantor_street_number::TEXT, '') || ' ' ||
          grantor_address || ' ' ||
          grantor_city || ', ' ||
          grantor_state || ' ' ||
          grantor_zip
        ) grantor_address,
        TRIM(
        
        ) grantee_address
        FROM wild.retr
    )
    SELECT * FROM addresses
  """


class GeocodeRetr(job.Job):
  def __init__(self, rerun_job_id=None, verbose=0) -> None:
    super().__init__(rerun_job_id, verbose)

  def execute(self, *args, **kwargs):
    self.stage_one()

  @job.stage
  def stage_one(self):
    addresses = query_addresses()
