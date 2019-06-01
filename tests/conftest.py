# Taken from tedi
from pathlib import Path
import os

here = os.path.abspath(os.path.dirname(__file__))

print("here: {}".format(here))

# fixtures_path = Path('ultron8/tests/fixtures').resolve()
fixtures_path = Path("tests/fixtures").resolve()
