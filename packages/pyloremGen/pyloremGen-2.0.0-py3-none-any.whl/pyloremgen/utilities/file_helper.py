""" Helper functions """

import json
import os
from pathlib import Path

BASEPATH = Path(os.path.dirname(__file__)).parents[0]
_path_file = os.path.join(BASEPATH, 'data/lorem_ipsum_wordlist.json')


def get_data_json(selection: str = 'lorem_words'):
    """Get data json"""
    with open(_path_file, encoding="utf-8") as file:
        data = json.load(file)
        data = data[selection]
    return data
