import dataclasses
import json
from dataclasses import dataclass


@dataclass
class Item:
    lat: float
    lon: float
    some_value: float
    id: str
    name: str


def parse_cities_data():
    # read raw chaos
    with open('misc/resp', 'rb') as f:
        data = f.read()

    # write valid JSON
    with open('misc/resp.json', 'w') as f:
        json.dump(data_dict := json.loads(data.decode('unicode-escape')), f)

    # extract cities
    values = data_dict[0]['values']['map']['x']['calls'][2]['args']

    # collect cities
    items = []
    for i in range(len(values[0])):
        items.append(Item(
            values[0][i],
            values[1][i],
            values[2][i],
            values[3][i],
            values[8][i]
        ))

    # write clean and valid
    with open('misc/cities.json', 'w') as f:
        json.dump(
            [dataclasses.asdict(i) for i in items],
            f
        )


def parse_match_response():

    with open('misc/closestcity', 'rb') as f:
        data = json.load(f)

    # write valid JSON
    with open('misc/closestcity.json', 'w') as f:
        json.dump(data, f)
