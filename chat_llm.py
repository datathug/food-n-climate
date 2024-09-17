import base64
import os
import time
from datetime import datetime

import requests

from common import logger, CHATGPT_TEMPERATURE, OPENAI_MODEL, Credentials, SYSTEM_PROMPT, GEOCODING_PROMPT, \
    TOKENS_COUNT_FILE
from definitions import PdoItem, PdoLocation

from openai import OpenAI
import tiktoken


class ChatGptApi(OpenAI):

    prev_messages: list
    last_call_elapsed: float    # seconds
    results: list

    encoder = tiktoken.encoding_for_model("gpt-4o")
    tokens_file = TOKENS_COUNT_FILE
    token_count: int = 0
    token_count_at_start: int = 0
    session_tokens_in: int = 0
    session_tokens_out: int = 0
    last_call_tokens: int = -1

    def __init__(self):
        super().__init__(api_key=Credentials.load().openai)
        self.prev_messages = []
        self.results = []
        self.load_token_count()
        self.chat.completions.create = self.count_tokens(self.chat.completions.create)  # wrap
        logger.info(f"{datetime.now().ctime()} OpenAI API client initiated")


    def load_token_count(self):
        if os.path.isfile(self.tokens_file):
            with open(self.tokens_file) as f:
                self.token_count_at_start = self.token_count = int(f.read())
                logger.info(f"Loaded token count of {self.token_count} used before")
        else:
            self.token_count_at_start = self.token_count = 0

    def record_tokens(self):
        if self.token_count:
            with open(self.tokens_file, 'w') as f:
                f.write(str(self.token_count))

    def count_tokens(self, f):

        """ Decorator for the actual call to the superclass's method. """

        def wrapper(*args, **kwargs):
            in_tokens = sum([len(self.encoder.encode(x['content'])) for x in kwargs['messages']])
            self.token_count += in_tokens
            self.session_tokens_in += in_tokens
            result = f(*args, **kwargs)
            self.results.append(result)
            try:
                out_tokens = sum([len(self.encoder.encode(x.message.content)) for x in result.choices])
                self.token_count += out_tokens
                self.session_tokens_out += out_tokens
                self.last_call_tokens = in_tokens + out_tokens
                self.record_tokens()
            finally:
                return result
        return wrapper

    def message(self, msg):
        result = self.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": msg,
                }
            ],
            model=OPENAI_MODEL,
            temperature=0.6
        )
        print(result.choices[0].message.content)

    # @staticmethod
    # def parse_enumerated_list(text: str) -> list[str]:
    #     return [x.split('.')[-1].strip() for x in text.split('\n')]

    def geocoding_prompt(self, msg: str = None, pdo: PdoItem = None, verbose: bool = False):
        assert msg or pdo, 'either one must be provided'
        if pdo:
            msg = GEOCODING_PROMPT.format(country=pdo.country_EN, product_name=pdo.name, product_type=pdo.type_long)

        b = time.perf_counter()
        completion = self.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": msg,
                }
            ],
            model=OPENAI_MODEL,
            temperature=CHATGPT_TEMPERATURE
        )
        self.last_call_elapsed = time.perf_counter() - b
        gpt_messages: list[str] = [x.message.content for x in completion.choices]

        # set and parse in place
        if pdo:
            pdo.gpt_municipalities = pdo.parse_gpt(messages=gpt_messages)

        log_msg = '{} s ({}): {} / {} | {} (and more)'.format(
        int(self.last_call_elapsed),
            len(completion.choices),    # number of choices returned
            self.last_call_tokens,
            self.token_count,
            gpt_messages[0].split('\n')[0] if not verbose else ''  # example result if not verbose
        )
        logger.info(log_msg)

        if verbose:     # print out full
            logger.info(f"{pdo.name} {pdo.country_EN.upper()} {pdo.pdo_id} ({pdo.type_long})" + '\n' + pdo.raw_gpt)
        return completion


class LlamaApi:

    model: str = """llama3.1"""
    host: str = """localhost"""
    port: int = 11434
    keep_alive: int = 2 * 60    # seconds
    endpoint: str = None

    def __init__(self, host=None, port=None):
        if host:
            self.host = host
        if port:
            self.port = port
        self.endpoint = f"http://{self.host}:{self.port}/api/generate"
        logger.info(f'Using {self.endpoint}')
        self.initialize_model()

    def initialize_model(self):
        # empty response
        resp = requests.post(self.endpoint, json={
            "model": self.model,
            "keep_alive": self.keep_alive
        })
        assert resp.status_code == 200, \
            f'could not initialize LLAMA model {self.model}\n{resp.json()["error"]}'
        logger.info(f'Model {self.model} initialized')

    def make_payload(self, prompt: str):
        assert prompt, 'invalid prompt'
        return {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": self.keep_alive
        }

    def message(self, prompt: str):
        b = time.perf_counter()
        resp = requests.post(self.endpoint, json=self.make_payload(prompt))
        elapsed_s = int(time.perf_counter() - b)
        try:
            logger.info(f"SUCCESS: <{resp.status_code}> {len(resp.text)} B {elapsed_s} s")
            return resp.json()['response']
        except Exception as e:
            logger.warning(f"FAILED: <{resp.status_code}> {resp.text} B {elapsed_s} s")
            return e

    def llama_georef(self, pdo: PdoLocation) -> PdoLocation:
        msg = self.message(
            """Your are a geography expect specializing in geography of protected designations of origin 
            also known as PDO in the European union. You must use your intuition and knowledge about products 
            and make a guess about the location where this product comes from. This location information 
            must be an address - like string, representing an area, municipality or town, then province or state 
            or region within a country, and product's home country itself. Follow the rules of address formatting. I will later use this 
            address for geocoding, so keep this in mind. Format your response like the following JSON string: 
            { 
                area: YOUR_GUESS,
                region: YOUR_GUESS,
                country: YOUR_GUESS
            } 
            Your response must only include this JSON string and nothing else. Pay attention to local context and
            provide address in national language of product's home country. You must only use names of places and 
            administrative units that are common in countries' local language. Do not use English names for locations, 
            provinces, countries and towns and so on. Do not include small units like house number and street and 
            postal code in the address. 
            """.replace('\n', ' ').replace('  ', ' ') +
            f'Now guess address reference for product named "{pdo.name}" from {pdo.country}'
        )
        pdo.address = msg
        return pdo
