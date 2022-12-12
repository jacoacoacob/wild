import csv
import zipfile
import os
import re
from datetime import datetime

import requests

from ..lib import query, copy_csv_to_table


def retr_date_to_postgres_date(job, row, column, row_number):
  value = row.get(column)
  if value:
    try:
      d = value.zfill(8)
      d = datetime.strptime(d, "%m%d%Y")
      d = datetime.strftime(d, "%Y-%m-%d")
      return d
    except Exception as exc:
      job.logger.warn(f"{column} {row_number} {type(exc)} {exc}")
  

@query(fetch="all")
def select_dates_recorded():
  return """
    SELECT
      DISTINCT
        DATE_PART('year', date_recorded)::TEXT ||
        LPAD(DATE_PART('month', date_recorded)::TEXT, 2, '0') AS date_recorded
    FROM
      fmc.retr
  """


def fetch_available_urls(job):
    """
    Fetch a list of currently available data download URIs
    from https://www.revenue.wi.gov/Pages/ERETR/data-home.aspx
    """
    dor_root_url = "https://www.revenue.wi.gov"
    try:
      response = requests.get(dor_root_url + "/Pages/ERETR/data-home.aspx")
    except Exception as exc:
      job.logger.warn({
        "message": "There was an error fetching download urls",
        "type": type(exc).__name__,
        "data": exc
      })
    return [
      dor_root_url + path
      for path 
      in re.findall(r"/SLFReportsHistSales/\w*\.zip", response.text)
    ]


def extract_date_from_url(url):
  return re.search(r"(\d+)CSV\.zip", url).group(1)


def get_urls_to_fetch(job):
  available_months = [
    { "date": extract_date_from_url(url), "url": url }
    for url
    in fetch_available_urls(job)
  ]
  stored_months = [
    row.get("date_recorded")
    for row
    in select_dates_recorded()
  ]
  return [
    month.get("url")
    for month
    in available_months
    if month.get("date") not in stored_months
  ]


def download_retr_csv_zip(job, url, zip_loc):
  job.logger.info(f"Fetching {url}")
  response = requests.get(url)
  job.logger.debug({ "response_status_code": response.status_code })
  out_path = os.path.join(zip_loc, extract_date_from_url(url))
  job.logger.info(f"Saving response to {out_path}.zip")
  with open(out_path + ".zip", "wb") as out:
    out.write(response.content)


def clean_retr_csv(job, filename, raw_loc, clean_loc):
  try:
    in_file_path = os.path.join(raw_loc, filename)
    out_file_path = os.path.join(clean_loc, filename)
    with open(in_file_path, "r", encoding="cp1250", newline="") as in_file:
      with open(out_file_path, "w") as out_file:
        reader = csv.DictReader(in_file)
        writer = csv.DictWriter(
          out_file,
          fieldnames=[name for name in reader.fieldnames if len(name.strip()) > 0]
        )
        job.logger.info(f"Writing {out_file.name}")
        writer.writeheader()
        for index, row in enumerate(reader):
          writer.writerow({
            **{
              col: row[col].strip()
              for col
              in row if len(col) > 0 
            },
            **{
              col: retr_date_to_postgres_date(
                job,
                row,
                col,
                index + 1,
              )
              for col
              in [
                "CertificationDate",
                "DateConveyed",
                "DateRecorded",
                "DeedDate",
                "GranteeCertificationDate",
              ]
            }
          })
        job.logger.info(f"Write complete")
  except Exception as exc:
    job.logger.warn(f"{type(exc)} {exc}")


def unpack_retr_csv(job, filename, zip_loc, unpack_loc):
  with zipfile.ZipFile(os.path.join(zip_loc, filename)) as zip_ref:
    # So this we coulllld just do `zip_ref.exractall(unpack_loc)` here
    # but given that we don't really have control over the zip archive origin,
    # I thinnnnk doing what we're doing below (doing some kind of filename 
    # validation before extraction) is what the docs recommend...
    # https://docs.python.org/3/library/zipfile.html?highlight=zipfile#zipfile.ZipFile.extractall
    for archive_member in zip_ref.namelist():
      if archive_member.startswith(filename[:6]):
        zip_ref.extract(archive_member, unpack_loc)
      else:
        job.logger.warn(
          f"Detected archive member with unexpected name '{archive_member}'. Extraction from zip arcive not attempted."
        )


def copy_retr_csv_to_database_table(job, csv_loc, csv_filename):
  try:
    # cp1250 is encoding used by Windows https://docs.python.org/3.10/library/codecs.html
    with open(os.path.join(csv_loc, csv_filename), "r", encoding="cp1250") as file:
      job.logger.info(f"Copying {csv_filename} to database")
      copy_csv_to_table(file, "fmc.retr")
      job.logger.info(f"Copy complete")
  except Exception as exc:
    job.logger.warn(f"{type(exc)} {exc}")
