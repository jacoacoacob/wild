from typing import List


class Muni:
  def __init__(self, county, tvc, prefix=[]) -> None:
    self.county = county
    self.tvc = tvc
    self.prefix = prefix



def muni_add(munis: List[Muni], county, tvc, prefixes):
  return munis + [Muni(county, tvc, prefixes)]


def tvc_replace(munis: List[Muni], county, old_tvc, new_tvc):
  return [
    Muni(m.county, new_tvc, m.prefix) if m.tvc == old_tvc else m
    for m
    in munis
  ]
    

def tvc_replace_many(munis: List[Muni], county, old_tvcs, new_tvc):
  pass


def tvc_variant(munis: List[Muni], county, orig_tvc, variant_tvc):
  pass


def county_variant(munis: List[Muni], orig_county, variant_county):
  pass


