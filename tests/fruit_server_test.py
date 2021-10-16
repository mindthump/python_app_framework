import pytest
import json
from unittest.mock import MagicMock
from .. import fruit_server as fruit
from toolbox import app_utils


def test_fruit_server():
    req = MagicMock()
    resp = MagicMock()
    fs = fruit.FruitServer()
    fs.on_get(req, resp)
    # We don't know which fruit, but we can see if it's a reasonable dict
    assert "favorite_fruit" in json.loads(resp.body)
    pass
