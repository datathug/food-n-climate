import json

from definitions import PdoItem
from pathlib import Path


GPT_GEOREFERENCES_DIR = 'data/gpt-georef'   # make sure it is the same
LENGTH_CUTOFF_GPT = 3   # min characters from gpt suggested address

def load_pdo_item(fp: Path):
    # assume exists
    with open(str(fp), encoding='utf-8') as f:
        item = PdoItem(**json.load(f))
        return item.pdo_id, item


def get_pdos() -> dict[str, PdoItem]:

    assert Path(GPT_GEOREFERENCES_DIR).is_dir(), f'could not find {GPT_GEOREFERENCES_DIR}'
    files = [x.resolve() for x in Path(GPT_GEOREFERENCES_DIR).glob('*.json')]

    return dict([load_pdo_item(fp) for fp in files])        # PDO-FR-02354: PdoItem


# make lowercase and no spaces
format_commune_name = lambda x: x.split(',')[0].strip().lower().replace(' ', '')

pdos: dict[str: PdoItem] = get_pdos()
REFERENCED_ADDRESSES: set[str] = set()
for p in pdos.values():
    REFERENCED_ADDRESSES = REFERENCED_ADDRESSES.union(set(
        [
            (commune, p.country_code) for x in p.municipalities
            if len(commune := format_commune_name(x)) >= LENGTH_CUTOFF_GPT
         ]
    ))

print(f'Read {len(REFERENCED_ADDRESSES)} unique commune references from {len(pdos)} PDO items')


def is_referenced(commune: str, country_code: str) -> bool:
    return (commune.strip().lower(), country_code) in REFERENCED_ADDRESSES
