import json

import requests

from common import CATEGORIES_JSON, RAW_CATEGORIES_JSON

CATEGORIES_URL = "https://www.tmdn.org/giview/api/geographical-indications/categories"
TARGET_LANGUAGE = 'EN'
VALID_LANGUAGES = ['BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'ES', 'ET', 'FI', 'FR', 'HR', 'HU', 'IT',
                   'LT', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SL', 'SV']


def get_name_in_lang_from_category_json(i: dict):
    return next(filter(lambda x: x['language'] == 'EN', i['translations']))['text']


def get_raw_categories():
    resp = requests.get(CATEGORIES_URL)
    assert resp.status_code == 200 and resp.content, 'bad response'

    data = resp.json()
    dump_to_json(data, RAW_CATEGORIES_JSON)
    return data


def clean_categories(raw_categories):
    return {
        int(i['id']): get_name_in_lang_from_category_json(i) for i in raw_categories
    }


def dump_to_json(categories: dict, outf: str):
    with open(outf, 'w') as fl:
        fl.write(json.dumps(categories))


def main():
    cats = clean_categories(get_raw_categories())   # mapping { int code: str category }
    dump_to_json(cats, CATEGORIES_JSON)
    return cats


if __name__ == '__main__':
    main()