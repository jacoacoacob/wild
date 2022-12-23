from typing import List


class Muni:
  def __init__(self, county, tvc, prefixes=[]) -> None:
    self.county: str = county
    self.tvc: str = tvc
    self.prefixes: List[str] = list(prefixes)

  def is_county_tvc(self, county, tvc):
    return self.county == county and self.tvc == tvc


class Municipalities:
  def __init__(self) -> None:
    self.data: List[Muni] = []

  def add_muni(self, county, tvc, prefixes):
    self.data.append(Muni(county, tvc, prefixes))

  def replace_tvc(self, county, old_tvc, new_tvc):
    self.data = [
      Muni(county, new_tvc, m.prefixes) if m.is_county_tvc(county, old_tvc) else m
      for m
      in self.data
    ]

  def replace_many_tvcs(self, county, old_tvcs, new_tvc, new_prefixes):
    old_tvcs = set(old_tvcs)
    filtered = [
      m
      for m
      in self.data
      if not (m.county == county and m.tvc in old_tvcs)
    ]
    self.data = filtered + [Muni(county, new_tvc, new_prefixes)]

  def add_tvc_variant(self, county, orig_tvc, variant_tvc):
    data = []
    for m in self.data:
      if m.is_county_tvc(county, orig_tvc):
        data += [m, Muni(county, variant_tvc, m.prefixes)]
      else:
        data.append(m)
    self.data = data

  def add_county_variant(self, orig_county, variant_county):
    self.data = self.data + [
      Muni(variant_county, m.tvc, m.prefixes)
      for m
      in self.data
      if m.county == orig_county
    ]

  def patch(self, config: dict):
    muni_add = config.get("muni_add", {})
    tvc_replace = config.get("tvc_replace", {})
    tvc_replace_many = config.get("tvc_replace_many", {})
    tvc_variant = config.get("tvc_variant", {})
    county_variant = config.get("county_variant", [])
    for county in muni_add:
      for tvc, prefixes in muni_add[county]:
        self.add_muni(county, tvc, prefixes)
    for county in tvc_replace:
      for old_tvc, new_tvc in tvc_replace[county]:
        self.replace_tvc(county, old_tvc, new_tvc)
    for county in tvc_replace_many:
      for old_tvcs, new_tvc, new_prefixes in tvc_replace_many[county]:
        self.replace_many_tvcs(county, old_tvcs, new_tvc, new_prefixes)
    for county in tvc_variant:
      for orig_tvc, variant_tvc in tvc_variant[county]:
        self.add_tvc_variant(county, orig_tvc, variant_tvc)
    for orig_county, variant_county in county_variant:
      self.add_county_variant(orig_county, variant_county)
