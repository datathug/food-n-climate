import time
import traceback
from pathlib import Path
from queue import Queue, Empty

from geopy import Location
from geopy.exc import GeocoderServiceError
from geopy.geocoders import GoogleV3

from common import logger, MAX_RETRIES, MAX_REQUESTS_PER_MINUTE, Credentials
from definitions import PdoItem


class Geocoder(GoogleV3):
    queue: Queue
    results: list[PdoItem]
    cache: dict   # str address : Location
    __min_time_between_requests: float = 60 / MAX_REQUESTS_PER_MINUTE    # seconds
    __last_request_timestamp: float = 0

    def __init__(self, check_api: bool = True) -> None:
        self.queue = Queue()
        self.results = []
        self.cache = {}

        super().__init__(api_key=Credentials.load().google, timeout=5)
        self.check_api() if check_api else None

    def geocode_batch(self, pdo_tasks: list[PdoItem]):

        if not pdo_tasks:
            return logger.warning('Empty batch came for geocoding')

        # populate q
        print(f'Received {len(pdo_tasks)} geocoding tasks')
        for i in pdo_tasks:
            self.queue.put(i)

        total_tasks = len(pdo_tasks)
        failed_count = 0

        started_batch = time.perf_counter()
        try:
            while not self.queue.empty():
                pdo_task: PdoItem = self.queue.get_nowait()

                # check retries
                if pdo_task.attempts >= MAX_RETRIES + 1:
                    self.results.append(pdo_task)  # append incomplete
                    continue

                pdo_task.attempts += 1  # keep track of attempts for each

                if (delta := (time.perf_counter() - self.__last_request_timestamp)) < self.__min_time_between_requests:
                    time.sleep(delta)   # wait respect API

                response: list[Location] = super().geocode(
                    pdo_task.address_nocountry, exactly_one=False,
                    components={'country': pdo_task.country}
                )

                if response:
                    pdo_task.set_result(location=response[0])
                    self.results.append(pdo_task)
                else:
                    pdo_task.status = 'failed'
                    # retry
                    self.queue.put_nowait(pdo_task)
                    failed_count += 1

                if self.results and ((res_count := len(self.results)) % 100 == 0 or res_count in [10, 20, 40, 60, 80]):
                    logger.info(f"{res_count} / {total_tasks} successfully processed, {failed_count} failed")

        except Empty:
            pass

        finally:
            total_elapsed = time.perf_counter() - started_batch
            m, s = divmod(int(total_elapsed), 60)
            logger.info(f"GEOCODING COMPLETED! Processed {len(self.results)} locations in {m} m {s} s")
        return self.results

    def geocode_with_cache(self, address: str) -> (float, float):

        # look up in cache first
        if address in self.cache:
            logger.info(f"Found cached value for {address}")
            return self.cache[address]

        begin = time.perf_counter()
        xy = self.geocode(address, exactly_one=True)
        self.__last_request_timestamp = time.perf_counter()
        elapsed = self.__last_request_timestamp - begin

        msg = "{} \t ({} ms) \t {} {}".format(
            'OK' if xy else 'FAILED',
            int(elapsed * 1000),
            address,
            tuple(round(i, 4) for i in xy)
        )
        logger.info(msg) if xy else logger.warning(msg)
        return xy

    def geocode(self, address: str, exactly_one: bool = True) -> (float, float):     # ignore warning from IDE

        if not exactly_one:
            raise NotImplemented('this geocoding approach supports exactly one point per address')

        try:

            response: Location = super().geocode(address, exactly_one=exactly_one)
            xy = self.cache[address] = response.longitude, response.latitude   # update cache

            logger.warning(
                f"Received multiple ({len(response)}) locations for '{address}'"
            ) if (isinstance(response, list) and len(response) > 1) else None

            return xy
        except GeocoderServiceError:
            logger.error(f"Exception caught when geocoding '{address}'")
            logger.error(traceback.format_exc())

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
