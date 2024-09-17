import threading
from queue import Queue, Empty
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import requests

from common import PDOS_JSON_FILE

N_THREADS = 4
RAW_DATA_DIR = 'data/raw'
TARGET_URL = "https://www.tmdn.org/giview/api/geographical-indications/{}"
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

RAW_DATA_DIR = Path(RAW_DATA_DIR)
assert RAW_DATA_DIR.exists(), f"could not find directory {str(RAW_DATA_DIR)}"
assert N_THREADS.is_integer() and 1 <= N_THREADS <= 8, f'invalid number of threads {N_THREADS}'


class ScrapingError(Exception):
    pass


@dataclass
class ScrapeItem:
    id: str     # sth like 'EUGI00000003101'
    data: dict = None
    scraped_at: datetime = None
    elapsed: float = -1   # ms

    def dump_to_file(self):
        self.data['id'] = self.id
        self.data['scraped_at'] = self.scraped_at.ctime()   # human readable
        self.data['timestamp'] = int(self.scraped_at.timestamp())   # UNIX timestamp, tz aware
        self.data['elapsed_ms'] = self.elapsed   # GET req
        with open(str(RAW_DATA_DIR / self.id) + '.json', 'w') as f:
            json.dump(self.data, f)


class GlViewScraper:

    complete_pdo: list[ScrapeItem]
    tasks: Queue[ScrapeItem]
    threads: []
    lock = threading.Lock()

    def __init__(self):
        self.complete_pdo = []
        self.session = requests.Session()
        self.tasks = Queue()
        self.populate_queue()

    def get_by_id(self, task_item: ScrapeItem):

        """

        :param task_item: sth with id attribute like 'EUGI00000003101'
        :return:
        """

        assert len(task_item.id) > 10, f'invalid id = {task_item.id}'
        url = TARGET_URL.format(task_item.id)
        b = time.perf_counter()
        task_item.scraped_at = datetime.now()
        resp = self.session.get(url)
        task_item.elapsed = round((time.perf_counter() - b) * 1000)
        logging.info(f"Get by ID = {task_item.id} - status {resp.status_code} \t{len(resp.content)} B ({task_item.elapsed} ms)")
        try:
            task_item.data = self.parse_json(response=resp)
        except ScrapingError as e:
            task_item.data = {"error": "scraping error. see log for details"}
        except Exception as e:
            task_item.data = {"error": "unknown exception. see log for details"}
        return task_item

    def parse_json(self, response: requests.Response):

        if response.status_code != 200:
            raise ScrapingError("Cannot parse response with status code != 200")

        if not response.headers['content-type'] == 'application/json':
            raise ScrapingError("Cannot parse response, expected 'application/json' as content-type in headers")
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise ScrapingError(e)

    def get_bulk_in_thread(self):
        counter = 0
        logger.info(f"{threading.current_thread().name} started")
        while True:
            try:
                # with self.lock:
                task = self.tasks.get(timeout=1)
                counter += 1
            except Empty:
                logger.info(f'All tasks complete in thread ({counter} total)')
                return

            self.complete_pdo.append(self.get_by_id(task_item=task))
            task.dump_to_file()     # do in thread

    def run(self):
        logger.info(f"Running in {N_THREADS} theads")
        self.threads = [threading.Thread(target=self.get_bulk_in_thread) for _N_THREADS in range(N_THREADS)]
        for t in self.threads:
            t.start()
        for t in self.threads:
            t.join()
        logger.info(f"All tasks complete. Writing to disk")

    def populate_queue(self):
        with open(PDOS_JSON_FILE) as f:
            pdos: list = json.loads(f.read())

        for i in pdos:
            self.tasks.put(ScrapeItem(id=i['id']))

        logger.info(f"Loaded {self.tasks.qsize()} items in queue")


if __name__ == '__main__':
    scraper = GlViewScraper()
    scraper.run()
