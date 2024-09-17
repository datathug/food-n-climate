import dataclasses
import json
from dataclasses import dataclass, field
from itertools import count
from pathlib import Path

# required for qgis import - only for PdoLocation class
try:
    from geopy import Point, Location
    from common import MAX_RETRIES, logger
except ImportError:
    Location = None
    Point = None
    logger = None
    MAX_RETRIES = -1


@dataclass
class GeorefUnit:

    """ Represents a point as per Geocode API with an address georef string attached. """

    georef: str
    lon: float
    lat: float
    pdo: str    # PDO-FR-A7865

    id: int = field(default_factory=count(1).__next__)  # autoincrement

    @staticmethod
    def as_dataframe(units: list):
        from pandas import DataFrame
        df = DataFrame([dataclasses.asdict(x) for x in units])
        # df.set_index('id', inplace=True)      # not yet!
        return df[df.columns[::-1]]     # id will be first


@dataclass
class PdoItem:

    """ Required for collecting georeferences a.k.a. "addresses" with ChatGPT. """

    # initialize with these
    pdo_id: str
    name: str
    country_EN: str     # do not use for geocoding, use country in local language derived from address
    type_long: str

    # populate later
    raw_gpt: str = ''     # raw response with delimiters
    municipalities: list[str] = None
    count: int = 0

    # will be populated with QGIS or geocoding
    locations: list[tuple[float, float]] = None
    attempts: int = 0

    def parse_gpt(self, messages: list[str]):
        self.municipalities = []
        for msg in messages:
            self.raw_gpt += '\n' if self.raw_gpt and self.raw_gpt[-1] != '\n' else ''
            self.raw_gpt = msg
            self.municipalities.extend(
                [x.split('.')[-1].strip() for x in msg.split('\n')]     # parse enumerated list
            )   # parse enumerated list
            self.count += len(self.municipalities)

    def to_file(self, directory: str):
        Path(directory).mkdir(parents=True, exist_ok=True)
        fp = Path(directory) / f'{self.pdo_id}.json'
        with open(str(fp), 'w') as f:
            f.write(json.dumps(dataclasses.asdict(self)))
            logger.info(f"{self.name}, {self.country_EN.upper()}: {len(self.municipalities)} addresses recorded")

    @property
    def country_code(self):
        cc = self.pdo_id.split('-')[1].upper()
        return cc if cc != 'GR' else 'EL'   # special case for Greece, uses both GR and EL


if Location:
    @dataclass
    class PdoLocation:
        pdo_id: str  # like PDO_IT_234567
        name: str   # Product name
        address: str = None
        country: str = None  # derived
        address_nocountry: str = None  # derived, without country - rsplit string!
        status: str = 'unprocessed'  # set later
        location: Location = None  # set later
        point: Point = None
        attempts: int = 0  # number of retries after first request failed
        gpt_response: str = None
        gpt_municipalities: list[str] = None

        def __post_init__(self):
            self.set_address(self.address) if self.address else None

        def set_address(self, address_georef: str):
            # TODO
            # assert self.address, 'invalid address'
            components = self.address.rsplit(',', maxsplit=1)
            if len(components) != 2:
                raise Exception(f'could not derive country from address "{self.address}"')

            if ',' in (initial_country := self.country) or not self.country:
                self.address_nocountry, self.country = [x.strip() for x in components]

                logger.warning(
                        f"Using country '{self.country}' instead of '{initial_country}' for {self.name} ({self.address})"
                    ) if initial_country != self.country else None
            else:
                self.address_nocountry = components[0]
                # if double like "Belgium, Netherlands" - use one from address string

        def set_result(self, location: Location) -> None:
            if isinstance(location, Location):
                self.status = 'OK'
                self.location = location
                self.point = location.point
            else:
                self.status = 'failed'

        def csv(self) -> str:
            return ','.join(
                [
                    self.pdo_id,
                    self.address_nocountry,
                    self.country,
                    self.status,
                    self.attempts < MAX_RETRIES,  # bool
                    json.dumps(self.location.raw),
                    self.point.longitude,  # lonlat format EPSG:4326
                    self.point.latitude
                ]
            )

        def json_serialized(self) -> str:
            return json.dumps({
                'id': self.pdo_id,
                'status': self.status,
                'attempts': self.attempts,
                'raw': self.location.raw
            }) if self.location else None