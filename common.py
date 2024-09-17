""" Global settings for the project. """

LOG_FILE = 'data/google-geocode-gpt-data.log'
PDOS_JSON_FILE = "data/pdos.json"
TOKENS_COUNT_FILE = 'tokens.count'
GPT_GEOREFERENCES_DIR = 'data/gpt-georef'

RAW_CATEGORIES_JSON = "data/raw_categories.json"
CATEGORIES_JSON = "data/categories.json"
CREDENTIALS_FILE = "credentials.json"


EAMBROSIA_CATALOG_CSV = 'data/eambrosia-full.csv'
GEOCODED_CSV = 'data/eambrosia_geocoded.csv'

GEOREF_UNITS_CSV = 'data/georef_units_xy.csv'

# OpenAI and ChatGPT settings
CHATGPT_TEMPERATURE = 0.5   # use smaller values for geocoding - no creativity
OPENAI_MODEL = 'gpt-4o'


# Google Geocode API settings
MAX_RETRIES = 2  # GOOGLE Geocoder - number of retries after first request failed
MAX_REQUESTS_PER_MINUTE = 600


# ChatGPT's system prompt that sets chat's behavior prior to user input
SYSTEM_PROMPT = """Your are an expert in geography of protected designations of origin 
            also known as PDO in the European union. You must use your knowledge about products produced in various PDO
            and make a guess about the geographic location of the PDO. This location information must include names of 
            municipalities, communes and other small administrative units in EU countries. Usually a PDO 
            encompasses several municipalities or communes. Do not include towns or villages or settlements in your 
            response, only administrative units. Provide the results as enumerated list of municipalities with exactly 
            one municipality per line. The output geographic reference of the PDO must be similar to an address, 
            featuring a province or department unit as well as its origin country name. 
            
            Provide output in the national language of the home country of the PDO. Do not use
            geographic names in English, use national names in their own language instead. You will be given names 
            of protected products coming from different PDOs and countries where these are located.
            Keep your response short and brief. Only include necessary information. Remember that all PDO information 
            is found on eAmbrosia website and in EU legal documents regarding 
            PDO from eur-lex.europa.eu, in multiple languages. Usually each PDO has a related legal document 
            published on eur-lex.europa.eu which has got a specific section about geographical area occupied by a PDO.
            Make emphasis on using this geographic information from documents. It may also contain names that are not
            considered part of a PDO. If so, do not include those. 
            Do not make up information and only output locations that you are completely sure are a part of a PDO. 
            """


# user prompt customized for each request
GEOCODING_PROMPT = """
Now give me geographic references in national language for municipalities that belong to a PDO in {country}, 
where {product_name} is produced. This product was classified as {product_type} in the EU nomenclature. 
Format your message so that each municipality is mentioned along with a province or state it is located in, 
in the same record after comma. Country name in its own language must be present last. 
Format output as an enumerated list."""

# formatting
SYSTEM_PROMPT = SYSTEM_PROMPT.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('   ', ' ')
GEOCODING_PROMPT = GEOCODING_PROMPT.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').replace('   ', ' ')


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
        with open(os.path.abspath(CREDENTIALS_FILE), "r") as f:
            logger.info(f"Using credentials from {CREDENTIALS_FILE}")
            # decode
            keys = json.load(f)
            for k in keys:
                keys[k] = base64.b64decode(keys[k]).decode('utf-8')
            return cls(**keys)
