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


def API_CONFIG(_GOOGLE_API_KEY: str = "", _GOOGLE_SEARCH_ENGINE_ID: str = "") -> None:
    global GOOGLE_SEARCH_ENGINE_ID, GOOGLE_API_KEY
    GOOGLE_API_KEY = _GOOGLE_API_KEY
    GOOGLE_SEARCH_ENGINE_ID = _GOOGLE_SEARCH_ENGINE_ID
    if CONF_DEBUG and _GOOGLE_API_KEY != "":
        logging.info(f"API_KEY set")
    if CONF_DEBUG and _GOOGLE_SEARCH_ENGINE_ID != "":
        logging.info(f"SEARCH_ENGINE_ID set")


def NLP_config(mode: str = "default", debug: bool = True) -> None:
    global conf_MODE, conf_DEBUG
    CONF_DEBUG = debug
    if mode == "accuracy" or mode == "speed":
        NLP_CONF_MODE = mode
    else:
        if CONF_DEBUG:
            logging.warn(f"mode: {mode} does not exist")
