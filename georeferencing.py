import json
import os.path

from common import GPT_GEOREFERENCES_DIR, logger, PRODUCT_TYPE_LONG, PRODUCT_NAME, FILE_NUMBER, COUNTRY
from definitions import PdoItem
from parse_eambrosia_dataset import load_and_prepare
from pathlib import Path

from gpt.georef_engine import ChatGptApi

# if true, does not repeat georeferencing for PDOs that already have the information in files
# overwrites provious results!
# helps save tokens as OpenAI charges under pay-as-you-go scheme
# as of Sep 14 2024, price is $5.00 per 1M tokens.
# Therefore, a single geocoding request as implemented here costs between $0.002 - $0.003
# Overall price for 1864 records dataset estimated around $4
OVERWRITE_EXISTING_DATA = False
COMPOUND_NAME = 'compound-pdos-georef.json'


def load_processed_ids() -> list[str]:
    files = Path(GPT_GEOREFERENCES_DIR).glob('*.json')
    return [f.name.replace(f.suffix, '') for f in files]


def make_compound():
    files = Path(GPT_GEOREFERENCES_DIR).glob('*.json')
    data = []
    for fp in files:
        # do not use self!
        if COMPOUND_NAME in str(fp.name):
            continue

        with open(str(fp.resolve()), 'r') as f:
            data.append(json.load(f))

    # sort before writing
    data.sort(key=lambda x: x['pdo_id'])

    # write all
    with open(os.path.join(GPT_GEOREFERENCES_DIR, COMPOUND_NAME), 'w') as f:
        f.write(json.dumps(data))


def make_compound_csv():
    import pandas as pd

    df = pd.read_json(os.path.join(GPT_GEOREFERENCES_DIR, COMPOUND_NAME))
    df.to_csv(COMPOUND_NAME, index=False)


def main():

    df = load_and_prepare(assert_georef=False)   # includes PDO column with empty address

    api = ChatGptApi()

    if not OVERWRITE_EXISTING_DATA:
        skip_ids = load_processed_ids()
        logger.info(f"Skipped {len(skip_ids)} georeferenced PDOs from {GPT_GEOREFERENCES_DIR}")
    else:
        logger.warning(f"RUNNING GEOREFERENCER IN CLEAN START MODE. MAY OVERWRITE PROCESSED JSON FILES. ")
        skip_ids = []

    for i, row in df.iterrows():

        if not OVERWRITE_EXISTING_DATA and row[FILE_NUMBER] in skip_ids:
            continue

        pdo = PdoItem(
            pdo_id=row[FILE_NUMBER],
            name=row[PRODUCT_NAME],
            country_EN=row[COUNTRY],
            type_long=row[PRODUCT_TYPE_LONG]
        )

        api.geocoding_prompt(pdo=pdo, verbose=True)     # receives and parses data in place
        pdo.to_file(directory=GPT_GEOREFERENCES_DIR)    # dump to .json file

    make_compound()


if __name__ == '__main__':
    main()
