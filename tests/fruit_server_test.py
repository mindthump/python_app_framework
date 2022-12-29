import pytest
import json
from unittest.mock import MagicMock
import fruit_server_app.fruit_server as fserver
from app_utils import utils


def test_fruit_server():
    req = MagicMock()
    resp = MagicMock()
    fs = fserver.FruitServer()
    fs.on_get(req, resp)
    # We don't know which fruit, but we can see if it's a reasonable dict
    assert "favorite_fruit" in json.loads(resp.text)
    pass
