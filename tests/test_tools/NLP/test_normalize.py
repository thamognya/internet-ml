import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent) + "/internet_nlp/tools")
from normalize import normalizer


def test_generic_text() -> None:
    assert (
        normalizer("Hello. I am the firs'fsdjfkeif'sffdm.cv/lfsff'[]")
        == "hello i am the firsfsdjfkeifsffdmcvlfsff"
    )


def test_real_text() -> None:
    # Ayanakoji did not say that
    assert (
        normalizer("Hello, what a lovely day. I hate this game said Ayanakoji")
        == "hello what a lovely day i hate this game said ayanakoji"
    )
