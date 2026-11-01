import os
from functools import cache

from openai import OpenAI

BASE_URL = "https://openrouter.ai/api/v1"


@cache
def get_openai_client() -> OpenAI:
    return OpenAI(base_url=BASE_URL, api_key=os.environ["OPENROUTER_API_KEY"])
