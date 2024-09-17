import dataclasses
import json
from pathlib import Path
import random

import pandas as pd

from common import GPT_GEOREFERENCES_DIR, logger, GEOREF_UNITS_CSV
from definitions import PdoItem, GeorefUnit
from googleapi.geocoder import Geocoder
from gpt_geocode import COMPOUND_NAME


APPEND_TO_PROGRESS = True       # will overwrite when False
FORCE_OVERWRITE = False
GEOREF_UNITS_CSV = str(Path(GEOREF_UNITS_CSV).resolve())


def load_items() -> list[PdoItem]:
    files = Path(GPT_GEOREFERENCES_DIR).glob('*.json')
    data: list[PdoItem] = []
    for fp in files:
        # do not use compound json!
        if COMPOUND_NAME in str(fp):
            continue

        with open(str(fp.resolve()), 'r') as f:
            data.append(PdoItem(**json.load(f)))
    addr_count = sum([len(x.municipalities) for x in data])
    logger.info(f'Retrieved {len(data)} PdoItems from disk. Total N adresses {addr_count}')
    return data


def unique_addresses(items: list[PdoItem]) -> set[str]:
    filterfunc = lambda x: (
                                # do not include empty of other bad
                                len(x) > 3 and 'here are' not in x and 'here is' not in x
                                and all([
                                    # avoid super long answers that are obviously malformed
                                    len(s.strip()) < 38 for s in x.split(',')
                                ])
    )
    unique = set()
    _ = [[unique.add(i) for i in x.municipalities if filterfunc(i)] for x in items]
    logger.info(f'{len(unique)} unique addresses')
    return unique


def finalize_drop_duplicates():

    """ Parses CSV with addresses and coordinate XY data to find and remove duplicate records.
    Saves clean output to a separate file. """

    df = pd.read_csv(GEOREF_UNITS_CSV)
    df.drop('id', axis=1, inplace=True)  # so it does not interfere
    no_dupl = df.drop_duplicates(subset=df.columns.tolist(), ignore_index=True)
    no_dupl.to_csv(GEOREF_UNITS_CSV.replace('.csv', '_no_dupl.csv'), index=False)
    logger.info(
        "Finalized {} unique addresses with PDO reference and XY coordinates, {} duplicates removed".format(
            len(no_dupl), len(df) - len(no_dupl)
        )
    )


items = load_items()
clean_addresses = unique_addresses(items)

# update items' municipality property that represents addresses, drop invalid ones
for i in items:
    i.municipalities = [x for x in i.municipalities if x in clean_addresses]


georef_units = []
recorded: pd.DataFrame = None
recorded_count = 0

api = Geocoder(check_api=True)


if not Path(GEOREF_UNITS_CSV).is_file():
    APPEND_TO_PROGRESS = False
    FORCE_OVERWRITE = True
else:
    # check if it needs to be overwritten, and if we need to throw error
    if not APPEND_TO_PROGRESS and FORCE_OVERWRITE:
        logger.warning(f'Geocoded {GEOREF_UNITS_CSV} already exists, will be overwritten')

    elif APPEND_TO_PROGRESS:
        # filter out processed
        recorded = pd.read_csv(GEOREF_UNITS_CSV)  # skip processed
        recorded_count = len(set(pd.read_csv(GEOREF_UNITS_CSV)['georef']))  # skip processed

    else:
        raise FileExistsError(f'results file with progress already exists at {Path(GEOREF_UNITS_CSV).name}')

logger.info(f'Skipping {recorded_count} found in progress CSV')

first_run = True
for i in items:
    for a in set(i.municipalities):     # reduce duplicates with set

        lonlat = None
        if recorded is not None and len(rec := recorded.loc[recorded['georef'] == a]) > 0:

            # address may be in recorded addresses but under different PDO ID - must check on subset
            if len(rec.loc[rec["pdo"] == i.pdo_id]) > 0:
                continue
            else:
                # address was geocoded but for a different PDO ID.
                # use value from before, all lon lat values should be same across subset
                lonlat = float(rec['lon'].iloc[0]), float(rec['lat'].iloc[0])    # we know at least one row is present
                # logger.info(f"Found lon lat from a different PDO with the same georeference (address)")

        lonlat = api.geocode_with_cache(address=a) if not lonlat else lonlat    # geocode if not found in dataset
        unit = GeorefUnit(georef=a, lon=lonlat[0], lat=lonlat[1], pdo=i.pdo_id)
        georef_units.append(unit)

        # update dataframe and backup to file every time
        if not first_run:
            GeorefUnit.as_dataframe([unit]).to_csv(GEOREF_UNITS_CSV, mode='a', header=False, index=False)

        else:
            first_run = False
            mode = 'w' if not APPEND_TO_PROGRESS and FORCE_OVERWRITE else 'a'
            GeorefUnit.as_dataframe([unit]).to_csv(GEOREF_UNITS_CSV, mode=mode, header=(mode == 'w'), index=False)  # first run

        # info message every 100
        if (count := len(api.cache)) % 2 == 0 and count > 0:
            logger.info(f'Processed {count} out of {len(clean_addresses)} addresses, '
                        f'{recorded_count} found on startup')


finalize_drop_duplicates()


"""
2495,PDO-FR-A0737,46.9497545,4.2994059,"Autun, Saône-et-Loire, France"
2496,PDO-FR-A0737,46.6297354,5.225366699999999,"Louhans, Saône-et-Loire, France"
2497,PDO-FR-A0737,47.48822,3.907721999999999,"Avallon, Yonne, France"
2498,PDO-FR-A0737,47.798202,3.573781,"Auxerre, Yonne, France"
2499,PDO-FR-A0737,48.20065,3.28268,"Sens, Yonne, France"
2500,PDO-ES-0112,39.47173830000001,-3.5332049,"Madridejos, Toledo, España"

14200,PDO-FR-0106,45.567979,6.668573899999999,"La Côte-d'Aime, Savoie, France"
13896,PDO-IT-A1170,39.9284423,8.5300563,"Cabras, Provincia di Oristano, Italia"
"""