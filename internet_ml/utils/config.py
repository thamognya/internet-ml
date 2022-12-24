import logging

logging.basicConfig(
    filename="config.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

# Global
NLP_CONF_DEBUG: bool = True
# NLP
NLP_CONF_MODE: str = "default"


def NLP_config(mode: str = "default", debug: bool = True) -> None:
    global conf_MODE, conf_DEBUG
    NLP_CONF_DEBUG = debug
    if mode == "accuracy" or mode == "speed":
        NLP_CONF_MODE = mode
    else:
        if NLP_CONF_DEBUG:
            logging.warn(f"mode: {mode} does not exist")
