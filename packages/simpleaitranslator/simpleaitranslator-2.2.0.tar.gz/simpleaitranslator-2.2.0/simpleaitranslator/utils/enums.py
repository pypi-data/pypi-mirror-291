from enum import Enum


class ChatGPTModelForTranslator(Enum):
    BEST_BIG_MODEL = "gpt-4o-2024-08-06"
    BEST_SMALL_MODEL = "gpt-4o-mini"
    GPT_4o = "gpt-4o-2024-08-06"
    GPT_4o_mini = "gpt-4o-mini"

    def __str__(self):
        return self.value