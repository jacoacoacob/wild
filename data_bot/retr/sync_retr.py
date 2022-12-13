"""
This module contains code to download, clean, and copy Real Estate Transfer 
Return data (https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx) to a 
postgres database.
"""
import os

import dotenv

from ..lib import Job, stage
from . import utils as retr_utils

dotenv.load_dotenv()
  

class SyncRetr(Job):
  def __init__(self, rerun_job_id=None, verbose=0) -> None:
    super().__init__(rerun_job_id, verbose)
    zip_loc, raw_loc, clean_loc = [
      os.path.join(self.artifacts_path, dirname)
      for dirname
      in ("zip", "raw", "clean")
    ]
    if not rerun_job_id:
      for location in [zip_loc, raw_loc, clean_loc]:
        os.mkdir(location)
    self.zip_loc = zip_loc
    self.raw_loc = raw_loc
    self.clean_loc = clean_loc

  def execute(self, *args, **kwargs):
    # self.download_csv_zip_files()
    # self.unpack_csv_data()
    # self.clean_csv_data()
    self.copy_cleaned_data_to_database()

  @stage
  def download_csv_zip_files(self):
    for url in retr_utils.get_urls_to_fetch(self):
      retr_utils.download_retr_csv_zip(self, url, self.zip_loc)

  @stage
  def unpack_csv_data(self):
    for filename in os.listdir(self.zip_loc):
      retr_utils.unpack_retr_csv(
        self,
        filename,
        zip_loc=self.zip_loc,
        unpack_loc=self.raw_loc
      )

  @stage
  def clean_csv_data(self):
    for file in os.listdir(self.raw_loc):
      retr_utils.clean_retr_csv(self, file, self.raw_loc, self.clean_loc)

  @stage
  def copy_cleaned_data_to_database(self):
    for filename in os.listdir(self.clean_loc):
      retr_utils.copy_retr_csv_to_database_table(
        self,
        self.clean_loc,
        filename
      )
