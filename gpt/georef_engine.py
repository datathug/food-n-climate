import json
import os
import time
from datetime import datetime
from hashlib import md5

from common import logger, CHATGPT_TEMPERATURE, OPENAI_MODEL, TOKENS_COUNT_FILE
from definitions import PdoItem, Credentials, Prompts

from openai import OpenAI, ChatCompletion

1271107

class ChatGptApi(OpenAI):

    prev_messages: list
    last_call_elapsed: float    # seconds
    results: list
    prompts: Prompts

    tokens_file = TOKENS_COUNT_FILE
    token_count: int = 0
    token_count_at_start: int = 0
    session_tokens_in: int = 0
    session_tokens_out: int = 0
    last_call_tokens: int = -1

    last_n_chars_for_key_strorage: int = 6

    def __init__(self):
        super().__init__(api_key=Credentials.load().openai_nata)
        self.prev_messages = []
        self.results = []
        self.load_token_count()
        # self.chat.completions.create = self.count_tokens(self.chat.completions.create)  # wrap
        logger.info(f"{datetime.now().ctime()} OpenAI API client initiated")
        self.prompts = Prompts.load()


    def load_token_count(self):
        if os.path.isfile(self.tokens_file):
            with open(self.tokens_file) as f:
                key_counts = json.load(f)
                self.token_count_at_start = self.token_count = key_counts.get(self.api_key_identifier, 0)
                logger.info(f"Loaded token count of {self.token_count} used before")
        else:
            self.token_count_at_start = self.token_count = 0

    @property
    def md5_key(self) -> str:
        return md5(bytes(self.api_key, 'utf-8')).hexdigest()

    @property
    def api_key_identifier(self):
        return "....{} ( MD5 {})".format(self.api_key[-self.last_n_chars_for_key_strorage:], self.md5_key)

    def record_tokens(self):
        if self.token_count and self.token_count != self.token_count_at_start:

            # create file if does not exist
            if not os.path.isfile(self.tokens_file):
                with open(self.tokens_file, 'w') as f:
                    f.write('{ }')  # write empty JSON to avoid JSONDecode error - only when empty or new file
                prev_state = {}

            else:
                with open(self.tokens_file, 'r') as f:
                    prev_state = json.load(f)

            prev_state[self.api_key_identifier] = self.token_count     # set updated value after request performed
            with open(self.tokens_file, 'w') as f:
                json.dump(prev_state, f)

    def perform_completion(self, *args, **kwargs):

        raw_comp = self.chat.completions.with_raw_response.create(*args, **kwargs)
        comp: ChatCompletion = raw_comp.parse()
        headers = raw_comp.headers
        self.results.append(comp)

        # TODO use headers info to keep track of tokens

        try:
            self.session_tokens_in += comp.usage.prompt_tokens
            self.session_tokens_out += comp.usage.completion_tokens
            self.token_count += comp.usage.total_tokens
            self.last_call_tokens = comp.usage.total_tokens
            self.record_tokens()
        finally:
            return comp

    def count_tokens(self, f):

        """ Decorator for the actual call to the superclass's method. """

        def wrapper(*args, **kwargs):
            comp: ChatCompletion = f(*args, **kwargs)
            self.results.append(comp)

            try:
                self.session_tokens_in += comp.usage.prompt_tokes
                self.session_tokens_out += comp.usage.completion_tokens
                self.token_count += comp.usage.total_tokens
                self.last_call_tokens = comp.usage.prompt_tokes
                self.record_tokens()
            finally:
                return comp
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
            msg = self.prompts.user.format(country=pdo.country_EN, product_name=pdo.name, product_type=pdo.type_long)

        b = time.perf_counter()
        completion = self.perform_completion(
            messages=[
                {
                    'role': 'system',
                    'content': self.prompts.system,
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

