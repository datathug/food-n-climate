from pathlib import Path

import pandas as pd

from common import logger, EAMBROSIA_CATALOG_CSV, ID, PRODUCT_NAME, COUNTRY, GEOGRAPHIC_REFERENCE, \
    FILE_NUMBER, JSON_SERIALIZED, STATUS_COL, LAT_COLUMN, LON_COLUMN, TMP_PDO_TASK_COL, PDOS_GEOREF_XY
from definitions import PdoLocation
from google.geocoder_api import Geocoder


def load_and_prepare(assert_georef=True) -> pd.DataFrame:

    """ Loads EAmbrosia XLSX dataset as pandas dataframe for future processing. """

    required_columns = [PRODUCT_NAME, COUNTRY]
    required_columns += [GEOGRAPHIC_REFERENCE] if assert_georef else []
    df = pd.read_csv(EAMBROSIA_CATALOG_CSV)

    # validate
    for i in required_columns:
        assert i in df.columns, f'could not find column "{i}" in CSV'

    # get rid of meta info below the table
    df = df[df[FILE_NUMBER].notnull()]

    logger.info(f'Loaded {len(df)} rows from CSV')

    # reorder columns in dataset for convenience
    columns_reordered = required_columns + [
        i for i in df.columns if i not in required_columns
    ]
    df = df[columns_reordered]
    df.set_index(df[ID], inplace=True)
    return df


def ____populate_pdo_data(df: pd.DataFrame) -> pd.DataFrame:

    """ """

    make_pdo_instance: callable = lambda row: PdoLocation(
        pdo_id=row[FILE_NUMBER],
        name=row[PRODUCT_NAME],
        address=row[GEOGRAPHIC_REFERENCE] if GEOGRAPHIC_REFERENCE in df.columns else None,
        country=row[COUNTRY]
    )

    df[TMP_PDO_TASK_COL] = df.apply(make_pdo_instance, axis=1)  # create task object
    return df


def geocode_with_google(df: pd.DataFrame):
    api = Geocoder(check_api=True)  # initialize
    api.geocode_batch(list(df[TMP_PDO_TASK_COL]))  # will update in place

    # define extractors
    get_lon: callable = lambda x: float(x[TMP_PDO_TASK_COL].point.longitude) if x[TMP_PDO_TASK_COL].point else None
    get_lat: callable = lambda x: float(x[TMP_PDO_TASK_COL].point.latitude) if x[TMP_PDO_TASK_COL].point else None
    get_status: callable = lambda x: x[TMP_PDO_TASK_COL].status
    get_json: callable = lambda x: x[TMP_PDO_TASK_COL].json_serialized()

    df[LON_COLUMN] = df.apply(get_lon, axis=1)
    df[LAT_COLUMN] = df.apply(get_lat, axis=1)
    df[STATUS_COL] = df.apply(get_status, axis=1)
    df[JSON_SERIALIZED] = df.apply(get_json, axis=1)

    df.drop(TMP_PDO_TASK_COL, axis=1, inplace=True)     # clear temp data
    return df


def dump_to_file(df: pd.DataFrame, filepath: str = PDOS_GEOREF_XY):
    # dump to CSV
    if Path(filepath).is_file():
        logger.warning(f'Output CSV will be overwritten')
    df.to_csv(filepath, index=False)
