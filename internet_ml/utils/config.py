import typing

import logging

logging.basicConfig(
    filename="config.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

# Global
CONF_DEBUG: bool = True
# NLP
CONF_MODE: str = "default"


def NLP_config(mode: str = "default", debug: bool = True) -> None:
    global conf_MODE, conf_DEBUG
    CONF_DEBUG = debug
    if mode == "accuracy" or mode == "speed":
        CONF_MODE = mode
    else:
        if CONF_DEBUG:
            logging.warn(f"mode: {mode} does not exist")
