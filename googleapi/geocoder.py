import json
import time
from dataclasses import dataclass
from pathlib import Path
from queue import Queue, Empty

from geopy import Location, Point
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import GoogleV3

from googleapi.google_credentials import GOOGLE_API_KEY
from config import logger, MAX_RETRIES


@dataclass
class PdoLocation:
    pdo_id: str  # like PDO_IT_234567
    address: str
    country: str = None  # derived
    address_nocountry: str = None  # derived, without country - rsplit string!
    status: str = 'unprocessed'  # set later
    location: Location = None  # set later
    point: Point = None
    attempts: int = 0  # number of retries after first request failed

    def __post_init__(self):
        assert self.address, 'invalid address'
        components = self.address.rsplit(',', maxsplit=1)
        if len(components) != 2:
            raise Exception(f'could not derive country from address "{self.address}"')
        self.address_nocountry, self.country = components

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


class Geocoder(GoogleV3):
    queue: Queue
    results: list[PdoLocation]
    results_single_queries: list[PdoLocation]

    def __init__(self, check_api: bool = True) -> None:
        self.queue = Queue()
        self.results = []
        self.results_single_queries = []

        super().__init__(api_key=GOOGLE_API_KEY, timeout=5)
        self.check_api() if check_api else None

    def geocode_batch(self, addresses: list[PdoLocation]):

        if not addresses:
            return logger.warning('Empty batch came for geocoding')

        # populate q
        print(f'Preparing {len(addresses)} to process')
        for i in addresses:
            self.queue.put(i)

        try:
            while not self.queue.empty():
                pdo_task: PdoLocation = self.queue.get_nowait()

                # check retries
                if pdo_task.attempts >= MAX_RETRIES + 1:
                    self.results.append(pdo_task)  # append incomplete

                pdo_task.attempts += 1  # keep track of attempts for each
                begin = time.perf_counter()
                response: Location = super().geocode(
                    pdo_task.address_nocountry, exactly_one=False,
                    components={'country': pdo_task.country}
                )
                elapsed = time.perf_counter() - begin

                pdo_task.set_result(location=response)  # inplace
                if response:
                    self.results.append(pdo_task)
                else:
                    # retry
                    self.queue.put_nowait(pdo_task)

                msg = f"{pdo_task.status} \t ({int(elapsed * 1000)} ms) \t {pdo_task.address_nocountry} ({pdo_task.country})"
                logger.info(msg) if pdo_task.status == 'OK' else logger.warning(msg)

        except Empty:
            pass

    def geocode(self, pdo_task: PdoLocation, exactly_one: bool = True) -> PdoLocation:     # ignore warning from IDE
        try:

            result: Location = super().geocode(
                pdo_task.address_nocountry, exactly_one=exactly_one,
                components={"country": pdo_task.country}
            )

            self.results_single_queries.append(pdo_task)
            pdo_task.set_result(location=result)
            return pdo_task
        except GeocoderTimedOut:
            logger.error(f"Timed out while geocoding {pdo_task.address}")

    def dump_to_csv(self, path: str):
        if not self.results:
            return logger.warning("No results to write to CSV")

        assert (pathobj := Path(path)).parent.exists() and pathobj.parent.is_dir(), \
            f"invalid output CSV file path {path}"
        logger.warning('Target CSV file exists, will overwrite...') if pathobj.is_file() else None

        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(
                [','.join(['pdo', 'address', 'country', 'status', 'max_retries', 'raw_json', 'lon', 'lat'])] +
                [i.csv() for i in self.results]
            )

        logger.info(f"Wrote {len(self.results)} results to {path}")

    def check_api(self):
        """ Dummy request to ensure API is working and key is valid. """

        response: Location = super().geocode(
            query='Berlin', components={"country": 'Germany'},
        )
        if not all([
            response,
            response.point
        ]):
            raise Exception(f'could not perform API check call, key {self.api_key[:5]}')
        else:
            logger.info(f'Google Geocoder API works, API key {self.api_key[:5]}... good')


if __name__ == '__main__':
    api = Geocoder(check_api=True)
