#!/usr/bin/env python

from lxml import html
import requests
import json

def map_id_to_county():
  page = requests.get('https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents')
  root = html.fromstring(page.content)

  # Maps ids (strings) to county names (strings)
  counties = {}

  for tr in root.xpath('//*[@id="mw-content-text"]/table[2]/tr'):
    row  = tr.xpath('td')
    if len(row) >= 2:
      id   = row[0].xpath('text()')[0]
      name = row[1].xpath('a/text()')[0]
      counties[id] = name

  return counties

d = map_id_to_county()

with open('counties.json', 'w') as outfile:
  json.dump(d, outfile)

print d
# TODO: serialize so we only have to run this once
