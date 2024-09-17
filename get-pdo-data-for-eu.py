import json
from pathlib import Path

import requests
import logging

from common import PDOS_JSON_FILE, CATEGORIES_JSON

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('scraper')

GET_PDOS_URL = "https://www.tmdn.org/giview/api/search"

payload = {
    "countries": [
        "AT",
        "BE",
        "BG",
        "CY",
        "CZ",
        "DE",
        "DK",
        "EE",
        "ES",
        "FR",
        "FI",
        "SK",
        "SI",
        "SE",
        "RO",
        "NL",
        "PL",
        "PT",
        "MT",
        "LV",
        "GR",
        "HU",
        "HR",
        "IT",
        "IE",
        "LT",
        "LU"
    ],
    "name": "pdo",
    "pageNumber": 1,
    "productTypes": [],
    "giTypes": [],
    "statuses": [],
    "agreementType": None,
    "euProtectionDateFrom": "",
    "euProtectionDateTo": "",
    "categories": [],
    "pageSize": "",
    "sortingDirection": None,
    "sortingField": None,
    "language": "EN",
    "aggregateResults": None
}


def load_categories():
    with open(CATEGORIES_JSON) as f:
        data = json.loads(f.read())
        return {int(k): data[k] for k in data}


def get_pdo_data_from_glview():
    resp = requests.post(url=GET_PDOS_URL, json=payload)
    logger.info(f"{resp.status_code} {len(resp.content)} B")
    data = resp.json()
    total_records = data['totalRecords']
    pdos = data['resultRecords']
    categories = load_categories()

    if len(pdos) == total_records:
        logger.info(f"Received {total_records} records")
    else:
        logger.warning(f"Received {len(pdos)} records while total {total_records} promised")

    for i in pdos:
        i.update(i['basicData'])
        i.pop('basicData')
        i['statusOuter'] = i.pop('status') if 'status' in i else None   # interferes with status from basicInfo
        i['category_id'] = int(i['categories'][0]) if len(i['categories']) >= 1 else None
        i['category'] = categories[i['category_id']] if i['category_id'] else None  # human readable
        i['all_categories'] = i.pop('categories')
        

        if len(i['mapLocations']) == 1:
            i['point'] = i['mapLocations'][0]['lon'], i['mapLocations'][0]['lat']
            i['multiple_geometries'] = False
        elif len(i['mapLocations']) == 0:
            i['point'] = None
            i['multiple_geometries'] = False
        else:
            i['point'] = i['mapLocations'][0]['lon'], i['mapLocations'][0]['lat']
            i['multiple_geometries'] = True

    logger.warning(f"File {PDOS_JSON_FILE} exists, will be overwritten") if Path(PDOS_JSON_FILE).exists() else None
    with open(PDOS_JSON_FILE, 'w') as f:
        fsize = f.write(json.dumps(pdos))

    geojson_as_features = PDOS_JSON_FILE.replace('json', 'geojson')
    fc = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'properties': {**i, **{'multiplePoints': True}} if len(i['mapLocations']) > 1 else i,
                'geometry': {
                    'type': 'Point',
                    'coordinates': (
                        i['mapLocations'][0]['lon'], i['mapLocations'][0]['lat'] if i['mapLocations'] else None
                    )
                }
            }
            for i in pdos
        ]
    }
    logger.warning(f"File {geojson_as_features} exists, will be overwritten") if Path(
        geojson_as_features).exists() else None
    with open(geojson_as_features, 'w') as f:
        fsize = f.write(json.dumps(fc))
    logger.info(f"FeatureCollection written to {geojson_as_features} ({fsize} B)")
    return pdos


def enrich_geometries(pdos: list[dict]):
    for i in pdos:
        lonlat = None
        try:
            lonlat = i['geometry']['coordinates'][0]
        except KeyError:
            pass
        i["map_locations"] = {
            "type": "Point",
            "coordinates": lonlat
        }


if __name__ == "__main__":
    pdos = get_pdo_data_from_glview()
