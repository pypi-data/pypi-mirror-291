from pydantic import BaseModel

from simpleaitranslator.utils.enums import ModelForTranslator
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI


class HowManyLanguages(BaseModel):
    number_of_languages: int



