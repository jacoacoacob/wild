"""
This module contains code to download, clean, and copy Real Estate Transfer 
Return data (https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx) to a 
postgres database.
"""
import os
import re
from typing import List

import dotenv
import requests

from . import queries

dotenv.load_dotenv()


def fetch_download_links() -> List[str]:
  """
  Fetch a list of currently available data download URIs
  from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx
  """
  dor_root_url = "https://www.revenue.wi.gov"
  response = requests.get(dor_root_url + "/Pages/ERETR/data-home.aspx")
  return [
    dor_root_url + path
    for path 
    in re.findall(r"/SLFReportsHistSales/\w*\.zip", response.text)
  ]


def extract_months_from_links(links: List[str]):
  """
  Derive a list of dates (formatted "YYYYMM") from a list of URIs fetchd 
  from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx
  """
  return [
    re.search(r"(\d+)CSV\.zip", link).group(1)
    for link
    in links
  ]


def main():
  pass
