from typing import Any, List, Tuple

import logging

logging.basicConfig(
    filename="config.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

# General
CONF_DEBUG: bool = True
# Google
GOOGLE_API_KEY: str = ""
GOOGLE_SEARCH_ENGINE_ID: str = ""
# NLP
NLP_CONF_MODE: str = "default"


class FullConfig:
    def __init__(self: Any) -> None:
        self.CONF_DEBUG: bool = True
        self.GOOGLE_API_KEY: str = ""
        self.GOOGLE_SEARCH_ENGINE_ID: str = ""
        self.NLP_CONF_MODE: str = "default"

    def general_config(self: Any, CONF_DEBUG: bool) -> None:
        self.CONF_DEBUG = CONF_DEBUG

    def google_config(
        self: Any, GOOGLE_API_KEY: str, GOOGLE_SEARCH_ENGINE_ID: str
    ) -> None:
        self.GOOGLE_API_KEY = GOOGLE_API_KEY
        self.GOOGLE_SEARCH_ENGINE_ID = GOOGLE_SEARCH_ENGINE_ID

    def NLP_config(self: Any, NLP_CONF_MODE: str = "default") -> None:
        if (
            NLP_CONF_MODE == "accuracy"
            or NLP_CONF_MODE == "speed"
            or NLP_CONF_MODE == "default"
        ):
            self.NLP_CONF_MODE = NLP_CONF_MODE


config = FullConfig()
