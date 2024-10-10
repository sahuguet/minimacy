import requests
import json

URL = "https://demo.transiter.dev/systems/us-ny-subway/stops"


""" The endpoint returns a lot of information about stations.
The result is paginated using `nextId` for the next page.
For each page, we extract the id, name and list of lines.

In most cases, each station is split into two `childStops`, identified using the N (north?) and S (south?) suffixes.
"""


def get_stops(first_id=101):
  url = URL+ f"?first_id={first_id}"
  print(url)
  data = requests.get(url).json()
  stops = [ { 'id': cs['id'], 'name': cs['name'], 'lines': [k['id'] for k in s['serviceMaps'][0]['routes']] } for s in data['stops'] for cs in s['childStops']]
  return (data.get('nextId'), stops)

more = 1
all_stops = []
while more:
  more, stops = get_stops(first_id=more)
  all_stops.extend(stops)


with open('all_stops.json', 'w') as f:
  json.dump(all_stops, f, indent=2)
