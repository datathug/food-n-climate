import pandas as pd

from common import EAMBROSIA_CATALOG_CSV, ID, logger
from parse_eambrosia_dataset import FILE_NUMBER, COUNTRY, PRODUCT_NAME


def set_index_eambrosia():
    df = pd.read_csv(EAMBROSIA_CATALOG_CSV)
    if ID not in df.columns:
        orig_backup = EAMBROSIA_CATALOG_CSV.replace('.csv', '-orig.csv')
        reduced = EAMBROSIA_CATALOG_CSV.replace('.csv', '-for-ai.csv')
        df.to_csv(orig_backup, index=False)  # backup original

        df.sort_values(by=FILE_NUMBER, ignore_index=True, inplace=True)  # re-order

        # update original
        df.to_csv(EAMBROSIA_CATALOG_CSV, index=True, index_label=ID)

        # also make a sliced version with selected columns for AI address making
        df[[PRODUCT_NAME, COUNTRY, ]].to_csv(
            reduced,  # smaller for AI
            index=True, index_label=ID
        )
        logger.info(
            f'Updated original eAmbrosia dataset with {ID} field and created a reduced version "{reduced}"'
            ' for AI address making'
        )
    else:
        logger.info(f'field {ID} already exists in the dataset, skipped')


if __name__ == '__main__':
    set_index_eambrosia()
