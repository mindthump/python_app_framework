import pytest
import json
from unittest.mock import MagicMock
from fruit_server_app import fruit_server
from toolbox import app_utils


def test_fruit_server():
    req = MagicMock()
    resp = MagicMock()
    fs = fruit_server.FruitServer()
    fs.on_get(req, resp)
    # We don't know which fruit, but we can see if it's a reasonable dict
    assert 'favorite_fruit' in json.loads(resp.body)
    pass