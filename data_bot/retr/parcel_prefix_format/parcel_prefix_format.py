"""
Generate a postgres INSERT statement to seed wild.retr_municipality_parcel_format
"""
import re
import json
from typing import List

import requests
from bs4 import BeautifulSoup, Tag

from .parsers import get_county, get_tvc_and_prefix, get_panel_tags
from .transformers import Muni, Municipalities


def fetch_parcel_prefix_format_html():
  # # PROD
  # response = requests.get("https://www.revenue.wi.gov/Pages/UST/parcels.aspx")
  # return response.text
  # DEV
  with open("sandbox_parcel_prefix_format.html") as html:
    return html.read()


def get_sql_values(munis: List[Muni]):
  return ",\n  ".join([
    f"('{m.tvc}', '{m.county}', ARRAY{m.prefixes})"
    for m
    in munis
  ])


def DANGEROUSLY_DESTRUCTIVELY_WRITE_SQL(sql):
  tmpl_path = "sandbox_4-table-parcel-prefix-format.template.txt"
  out_path = "schema/deploy/4-create-table-retr-municipality-parcel-format.sql"
  with open(tmpl_path) as tmpl_file:
    template = tmpl_file.read()
    template = template.replace("%insert%", sql)
    with open(out_path, "w") as out_file:
      out_file.write(template)


def get_municipalities(soup: BeautifulSoup):
  munis = Municipalities()
  panel_tags: List[Tag] = get_panel_tags(soup)
  for panel in panel_tags:
    county = get_county(panel)
    for tvc_prefix_dict in get_tvc_and_prefix(panel):
      munis.add_muni(county, tvc_prefix_dict["tvc"], tvc_prefix_dict["prefix"])
  munis.patch({
    "muni_add": {
      "BROWN": [
        ("DE PERE, CITY OF", ["ED-", "WD-"])
      ],
      "KENOSHA": [
        ("SALEM, TOWN OF", ["65-4-120-", "66-4-120-", "67-4-120-"]),
        ("SILVER LAKE, VILLAGE OF", ["75-4-120-"]),
      ],
      "MARATHON": [
        ("BROKAW, VILLAGE OF", ["106-"])
      ],
      "OUTAGAMIE": [
        ("GREENVILLE, TOWN OF", ["110"]),
      ],
      # "OZAUKEE": [
      #   ()
      # ],
      "WAUKESHA": [
        ("WAUKESHA, TOWN OF", ["WAKT"]),
      ],
    },
    "tvc_replace": {
      "CHIPPEWA": [
        ("LAKE HOLCOMBE,TOWN OF", "LAKE HOLCOMBE, TOWN OF"),
      ],
      "DOOR": [
        ("JACKSONPOST, TOWN OF", "JACKSONPORT, TOWN OF"),
      ],
      "MARINETTE": [
        ("NAGARA, CITY OF", "NIAGARA, CITY OF"),
      ],
    },
    "tvc_variant": {
      "FOND DU LAC": [
        ("NORTH FOND DU LAC, VILLAGE OF", "NORTH FOND DU LAC, VILLAGE"),
      ],
      "KENOSHA": [
        ("PLEASANT PRAIRIE, VILLAGE OF", "PLEASANT PRAIRIE, VILLAGE"),
      ],
      "WAUKESHA": [
        ("MENOMONEE FALLS, VILLAGE OF", "MENOMONEE FALLS, VILLAGE O"),
      ],
    },
    "county_variant": [
      ("SAINT CROIX", "ST. CROIX")
    ]
  })
  return munis


def get_parcel_prefix_format():
  parcel_prefix_html = fetch_parcel_prefix_format_html()
  soup = BeautifulSoup(parcel_prefix_html, "html.parser")
  munis = get_municipalities(soup)
  sql_values = get_sql_values(munis.data)
  sql = f"""
INSERT INTO wild.retr_municipality_parcel_format
  (tvc_name, county_name, prefix)
VALUES
  {sql_values};
"""
  DANGEROUSLY_DESTRUCTIVELY_WRITE_SQL(sql)
