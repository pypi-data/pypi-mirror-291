# Adapted from https://github.com/statisticsnorway/microdata-tools/blob/master/microdata_tools/validation/components/unit_type_variables/__init__.py
# Under MIT License
# Copyright (c) 2023 Statistics Norway

from copy import deepcopy
from pathlib import Path

from kudaflib.logic.exceptions import InvalidIdentifierType
from kudaflib.logic.utils import load_json


UNIT_TYPE_VARIABLES_DIR = Path(__file__).parent
UNIT_TYPE_VARIABLES = {
    "KOMMUNE": load_json(UNIT_TYPE_VARIABLES_DIR / "KOMMUNE.json"),             # KUDAF added
    "FYLKE": load_json(UNIT_TYPE_VARIABLES_DIR / "FYLKE.json"),                 # KUDAF added
    "FYLKESKOMMUNE": load_json(UNIT_TYPE_VARIABLES_DIR / "FYLKESKOMMUNE.json"), # KUDAF added
    "PERSON": load_json(UNIT_TYPE_VARIABLES_DIR / "PERSON.json"),
    "ORGANISASJON": load_json(UNIT_TYPE_VARIABLES_DIR / "ORGANISASJON.json"),
}


def get(unit_type: str):
    try:
        return deepcopy(UNIT_TYPE_VARIABLES[unit_type])
    except KeyError as e:
        raise InvalidIdentifierType(unit_type) from e
