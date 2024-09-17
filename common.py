""" Global settings for the project. """

# Files and paths
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
# GEOCODED_CSV = 'data/eambrosia_geocoded.csv'
PDOS_GEOREF_XY = 'data/pdo_georef_xy.csv'

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
import logging


# logging configuration - write to file and console
LOGGER_FORMAT = "%(levelname)s:  %(message)s"
logger = logging.getLogger('')
logging.basicConfig(filename=LOG_FILE, filemode='a',
                    level=logging.INFO, format=LOGGER_FORMAT)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(LOGGER_FORMAT))
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)
