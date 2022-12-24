import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent) + "/internet_nlp/tools/data")
from internet import google


def test_generic_text() -> None:
    assert google("who is ronaldo") != google("who is messi")
