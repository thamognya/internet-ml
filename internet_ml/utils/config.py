import logging

logging.basicConfig(
    filename="config.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

GOOGLE_API_KEY: str = ""
GOOGLE_SEARCH_ENGINE_ID: str = ""

# Global
NLP_CONF_DEBUG: bool = True
# NLP
NLP_CONF_MODE: str = "default"


def API_CONFIG(_GOOGLE_API_KEY: str = "", _GOOGLE_SEARCH_ENGINE_ID: str = "") -> None:
    global GOOGLE_SEARCH_ENGINE_ID, GOOGLE_API_KEY
    GOOGLE_API_KEY = _GOOGLE_API_KEY
    GOOGLE_SEARCH_ENGINE_ID = _GOOGLE_SEARCH_ENGINE_ID


def NLP_config(mode: str = "default", debug: bool = True) -> None:
    global conf_MODE, conf_DEBUG
    NLP_CONF_DEBUG = debug
    if mode == "accuracy" or mode == "speed":
        NLP_CONF_MODE = mode
    else:
        if NLP_CONF_DEBUG:
            logging.warn(f"mode: {mode} does not exist")
