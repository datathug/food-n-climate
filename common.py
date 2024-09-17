""" Global settings for the project. """

LOG_FILE = 'data/google-geocode-gpt-data.log'
TOKENS_COUNT_FILE = 'tokens.count'
GPT_GEOREFERENCES_DIR = 'data/gpt-georef'
PDOS_JSON_FILE = "data/pdos.json"   # from GlView

RAW_CATEGORIES_JSON = "data/raw_categories.json"
CATEGORIES_JSON = "data/categories.json"
CREDENTIALS_FILE = "credentials.json"

# columns a.k.a. fields in eAmbrosia dataset from spreadsheet * * * * * * * * * * * * * * * * * * * * * * * * *
# REQUIRED COLUMNS IN INPUT
ID = 'ID'   # ID column integer autoincrement
FILE_NUMBER = 'File number'
COUNTRY = 'Country'
PRODUCT_NAME = 'Name'
# PRODUCT_TYPE_SHORT = 'Product type'    # only Food or Wine
PRODUCT_TYPE_LONG = 'Product category (obsolete)'
GEOGRAPHIC_REFERENCE = 'Georef'    # a.k.a. address to feed to Geocoding API

# COLUMNS TO BE CREATED BY SCRIPT FOR OUTPUT
LON_COLUMN = 'lon'  # Coordinate order Lon, Lat
LAT_COLUMN = 'lat'
STATUS_COL = 'GeocodingStatus'
JSON_SERIALIZED = 'json'

# TEMPORARY COLUMN WITH PYTHON OBJECTS, DROP IN THE END
TMP_PDO_TASK_COL = 'TMP_PDO_TASK'

EAMBROSIA_CATALOG_CSV = 'data/eambrosia-full.csv'
GEOCODED_CSV = 'data/eambrosia_geocoded.csv'
GEOREF_UNITS_CSV = 'data/georef_units_xy.csv'

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# OpenAI and ChatGPT settings
CHATGPT_TEMPERATURE = 0.5   # use smaller values for geocoding - no creativity
OPENAI_MODEL = 'gpt-4o'

SYSTEM_PROMPT_FILE = 'system.prompt'    # ChatGPT's system prompt that sets chat's behavior prior to user input
USER_PROMPT_FILE = 'user.prompt'    # user prompt customized for each request

# Google Geocode API settings
MAX_RETRIES = 2  # GOOGLE Geocoder - number of retries after first request failed
MAX_REQUESTS_PER_MINUTE = 600

# * * * * * * * * * * * * * *


import base64
import json
import logging
import os.path
from dataclasses import dataclass


# logging configuration - write to file and console
LOGGER_FORMAT = "%(levelname)s:  %(message)s"
logger = logging.getLogger('')
logging.basicConfig(filename=LOG_FILE, filemode='a',
                    level=logging.INFO, format=LOGGER_FORMAT)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(LOGGER_FORMAT))
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)


@dataclass
class Credentials:
    google: str
    openai: str

    @classmethod
    def load(cls):
        fp = os.path.abspath(CREDENTIALS_FILE)
        assert os.path.isfile(fp), f'Credentials file {fp} does not exist'
        with open(fp, "r") as f:
            logger.info(f"Using credentials from {CREDENTIALS_FILE}")
            # decode
            keys = json.load(f)
            for k in keys:
                keys[k] = base64.b64decode(keys[k]).decode('utf-8')
            return cls(**keys)


@dataclass
class PROMPTS:

    system: str
    user: str

    @classmethod
    def load(cls):
        fp = os.path.abspath(SYSTEM_PROMPT_FILE)
        assert os.path.isfile(fp), f'{fp} does not exist'
        with open(fp, "r") as f:
            system = f.read()

        fp = os.path.abspath(USER_PROMPT_FILE)
        assert os.path.isfile(fp), f'{fp} does not exist'
        with open(fp, "r") as f:
            user = f.read()

        assert system and user, 'invalid prompts'
        logger.info(f"Loaded ChatGPT prompts from files {SYSTEM_PROMPT_FILE}  {USER_PROMPT_FILE}")
        return cls(
            # ensure formatting
            system.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('   ', ' '),
            user.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('   ', ' ')
        )
