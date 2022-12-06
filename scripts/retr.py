"""
This module contains code to download, clean, and copy Real Estate Transfer 
Return data (https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx) to a 
postgres database.
"""
import re
import json
from typing import List

import dotenv
import requests

from . import queries
from .lib import Job

dotenv.load_dotenv()

# JOB_ARTIFACTS_PATH = os.getenv("JOB_ARTIFACTS_PATH", "jobs")


def fetch_download_links(*args, **kwargs) -> List[str]:
  """
  Fetch a list of currently available data download URIs
  from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx
  """
  dor_root_url = "https://www.revenue.wi.gov"
  try:
    response = requests.get(dor_root_url + "/Pages/ERETR/data-home.aspx")
  except Exception as exc:
    print(f"[retr::fetch_download_links] {type(exc).__name__}", exc)
  return [
    dor_root_url + path
    for path 
    in re.findall(r"/SLFReportsHistSales/\w*\.zip", response.text)
  ]


def extract_months_from_links(links: List[str], *args, **kwargs):
  """
  Derive a list of dates (formatted "YYYYMM") from a list of URIs fetchd 
  from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx
  """
  return [
    re.search(r"(\d+)CSV\.zip", link).group(1)
    for link
    in links
  ]


def sync_retr(*args, **kwargs):
  job = Job(verbose=kwargs.pop("verbose", 0))
  job.logger.info(json.dumps(dict(name="jacob")))
