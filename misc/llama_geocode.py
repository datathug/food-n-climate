import random

from parse_eambrosia_dataset import *


def llama_geocode():
    from chat_llm import LlamaApi

    api = LlamaApi(port=11555)

    df = populate_pdo_data(load_and_prepare())  # includes PDO column
    pdos: list = list(df[TMP_PDO_TASK_COL])

    geocode_random_pdo = lambda: api.llama_georef(random.choice(pdos))


